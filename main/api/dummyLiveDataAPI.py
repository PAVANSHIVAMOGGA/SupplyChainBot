"""
mock_live_service.py — Minimal mock live-data service for the supply chain agent project.

Two trackers, kept deliberately simple:
1. Inventory levels  -> GET /inventory/{sku}
2. Shipment status   -> GET /shipment/{shipment_id}

"Live" behavior is simulated with a small random walk applied on each request
(no background scheduler needed) so repeated calls show genuinely changing data,
plus a fixed set of failure/edge cases you can trigger on purpose for testing
your agent's error handling (see NOTES at the bottom).

Run:
    pip install fastapi uvicorn --break-system-packages
    uvicorn mock_live_service:app --reload --port 8001

Try:
    curl http://localhost:8001/inventory/ABC-RM-2210
    curl http://localhost:8001/shipment/SHP-1001
"""

import random
import time
import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ABC Mock Live Data Service")

# ---------------------------------------------------------------------------
# In-memory "database" — seeded with a few known SKUs / shipments so your
# agent has stable, repeatable things to query, plus room to test edge cases.
# ---------------------------------------------------------------------------

INVENTORY_DB = {
    "ABC-RM-2210": {"quantity": 4200, "unit": "units", "warehouse": "DC-03"},
    "ABC-FG-1001": {"quantity": 850, "unit": "units", "warehouse": "DC-01"},
    "ABC-FG-1002": {"quantity": 30, "unit": "units", "warehouse": "DC-01"},   # intentionally low, for stockout-risk testing
    "ABC-PK-5501": {"quantity": 0, "unit": "units", "warehouse": "DC-05"},   # intentionally zero, for out-of-stock testing
}

SHIPMENT_DB = {
    "SHP-1001": {"status": "in_transit", "origin": "Shenzhen", "destination": "DC-01", "eta_days": 4},
    "SHP-1002": {"status": "delayed", "origin": "Rotterdam", "destination": "DC-03", "eta_days": 9},
    "SHP-1003": {"status": "delivered", "origin": "Los Angeles", "destination": "DC-05", "eta_days": 0},
}

# Rough unit cost per SKU — needed so a reorder request can compute a total cost,
# which your graph will use to decide which approval tier applies (per POL-PROC-001).
UNIT_COST = {
    "ABC-RM-2210": 4.50,
    "ABC-FG-1001": 22.00,
    "ABC-FG-1002": 18.75,
    "ABC-PK-5501": 1.20,
}

# Orders "database" — append-only, doubles as the audit trail.
# Keyed by idempotency_key so a repeated request with the same key returns
# the original result instead of placing a duplicate order.
ORDERS_DB = {}

# Track when each item was last "refreshed" so responses can report data freshness
_last_updated = {}


def _touch(key: str):
    _last_updated[key] = datetime.utcnow()


def _freshness_seconds(key: str) -> int:
    last = _last_updated.get(key)
    if last is None:
        return 0
    return int((datetime.utcnow() - last).total_seconds())


# ---------------------------------------------------------------------------
# Inventory tracker
# ---------------------------------------------------------------------------

@app.get("/inventory/{sku}")
def get_inventory(sku: str):
    sku = sku.upper()

    if sku not in INVENTORY_DB:
        raise HTTPException(status_code=404, detail=f"SKU '{sku}' not found in inventory system.")

    record = INVENTORY_DB[sku]

    # Simulate a real system occasionally being flaky (~5% of calls)
    if random.random() < 0.05:
        raise HTTPException(status_code=503, detail="Inventory system temporarily unavailable. Try again shortly.")

    # Small random walk so quantity genuinely drifts call to call, but never below 0
    delta = random.randint(-15, 15)
    record["quantity"] = max(0, record["quantity"] + delta)
    _touch(sku)

    return {
        "sku": sku,
        "quantity": record["quantity"],
        "unit": record["unit"],
        "warehouse": record["warehouse"],
        "last_updated_seconds_ago": _freshness_seconds(sku),
    }


# ---------------------------------------------------------------------------
# Shipment status tracker
# ---------------------------------------------------------------------------

STATUS_PROGRESSION = ["in_transit", "customs_clearance", "delivered"]


@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: str):
    shipment_id = shipment_id.upper()

    if shipment_id not in SHIPMENT_DB:
        raise HTTPException(status_code=404, detail=f"Shipment '{shipment_id}' not found.")

    record = SHIPMENT_DB[shipment_id]

    if random.random() < 0.05:
        raise HTTPException(status_code=503, detail="Tracking system temporarily unavailable. Try again shortly.")

    # Occasionally nudge eta_days down to simulate real progression, unless already delivered
    if record["status"] != "delivered":
        record["eta_days"] = max(0, record["eta_days"] - random.choice([0, 0, 1]))
        if record["eta_days"] == 0 and record["status"] != "delayed":
            record["status"] = "delivered"

    _touch(shipment_id)

    return {
        "shipment_id": shipment_id,
        "status": record["status"],
        "origin": record["origin"],
        "destination": record["destination"],
        "eta_days": record["eta_days"],
        "last_updated_seconds_ago": _freshness_seconds(shipment_id),
    }


# ---------------------------------------------------------------------------
# Reorder — the write/action endpoint, intended for use behind a human-in-the-loop
# approval step in your graph, not called directly without confirmation.
# ---------------------------------------------------------------------------

class ReorderRequest(BaseModel):
    quantity: int
    idempotency_key: str | None = None  # pass the same key on retry to avoid duplicate orders


@app.post("/inventory/{sku}/reorder")
def reorder_sku(sku: str, request: ReorderRequest):
    sku = sku.upper()

    if sku not in INVENTORY_DB:
        raise HTTPException(status_code=404, detail=f"SKU '{sku}' not found in inventory system.")

    if request.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be a positive integer.")

    # Idempotency check — same key seen before -> return the original result, don't duplicate
    if request.idempotency_key and request.idempotency_key in ORDERS_DB:
        existing = ORDERS_DB[request.idempotency_key]
        return {**existing, "duplicate_request": True}

    # Simulate the order-placement system occasionally failing (~5%),
    # distinct from the approval step itself failing.
    if random.random() < 0.05:
        raise HTTPException(status_code=503, detail="Order placement system temporarily unavailable. Try again shortly.")

    unit_cost = UNIT_COST.get(sku, 10.00)
    total_cost = round(unit_cost * request.quantity, 2)
    order_id = f"PO-{uuid.uuid4().hex[:8].upper()}"
    key = request.idempotency_key or order_id

    order_record = {
        "order_id": order_id,
        "sku": sku,
        "quantity": request.quantity,
        "unit_cost": unit_cost,
        "total_cost": total_cost,
        "status": "placed",
        "placed_at": datetime.utcnow().isoformat(),
        "duplicate_request": False,
    }

    ORDERS_DB[key] = order_record

    # Reflect the order in current stock immediately, for simplicity —
    # a more realistic version would keep it as "incoming" until a separate
    # receiving event, mirroring your actual SOP-WH-IN-001 flow.
    INVENTORY_DB[sku]["quantity"] += request.quantity
    _touch(sku)

    return order_record


@app.get("/orders")
def list_orders():
    """Audit trail — every order ever placed, for verifying what actually executed."""
    return {"orders": list(ORDERS_DB.values())}


@app.get("/")
def root():
    return {
        "service": "ABC Mock Live Data Service",
        "trackers": ["/inventory/{sku}", "/shipment/{shipment_id}"],
        "actions": ["POST /inventory/{sku}/reorder"],
        "audit": ["/orders"],
        "sample_skus": list(INVENTORY_DB.keys()),
        "sample_shipments": list(SHIPMENT_DB.keys()),
    }