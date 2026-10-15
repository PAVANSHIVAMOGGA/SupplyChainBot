---
doc_id: SOP-WH-IN-001
title: Warehouse Inbound Receiving — Standard Operating Procedure
category: sop
department: Warehouse Operations
version: 2.4
status: active
effective_date: 2026-02-01
last_reviewed: 2026-02-01
owner: Warehouse Operations Manager
---

# ABC Corporation — Warehouse Inbound Receiving SOP

## Purpose
To ensure all inbound shipments are received, inspected, and recorded consistently across all ABC distribution centers, minimizing receiving errors and inventory discrepancies.

## Applicable Facilities
All ABC Distribution Centers (DC-01 through DC-07) and third-party logistics (3PL) partner sites operating under ABC's warehouse management system (WMS).

## Step-by-Step Procedure

### Step 1: Pre-Arrival Verification
- Confirm the Advance Shipping Notice (ASN) has been received in the WMS at least 4 hours prior to truck arrival.
- Cross-check ASN line items against the original Purchase Order (PO) number.
- Assign a dock door and receiving team via the dock scheduling system.

### Step 2: Dock Check-In
- Verify carrier seal number matches the ASN seal record. **Do not break the seal before this verification.**
- Record trailer condition (temperature-controlled loads require reefer log printout).
- Any seal mismatch or trailer damage must be logged as a Receiving Exception (Form REC-EX-01) before unloading begins.

### Step 3: Unloading and Piece Count
- Unload using standard pallet-jack or forklift protocol per Facility Safety Guidelines.
- Perform piece count against ASN. Discrepancies of more than 2% trigger a full recount and Receiving Exception filing.
- Damaged units are segregated immediately to the Damage Hold Area (DHA) and photographed.

### Step 4: Quality Spot-Check
- A minimum of 5% of received units (or 10 units, whichever is greater) must undergo visual quality inspection per POL-QA-004.
- Lots failing spot-check inspection are placed on Quality Hold and Procurement + Supplier Quality are notified within 2 business hours.

### Step 5: System Receipt (GRN Generation)
- Receiving clerk generates the Goods Receipt Note (GRN) in the WMS, referencing PO number, ASN number, and quantities actually received (not ordered).
- GRN quantity must match physical count, not PO quantity, if a discrepancy exists — discrepancies are noted in the GRN comments field for the 3-way match process (see POL-PROC-001, Section 5).

### Step 6: Putaway
- System-directed putaway location is followed unless a manual override is approved by the shift supervisor.
- Hazardous or temperature-sensitive goods must be moved to designated zones within 30 minutes of GRN completion.

## Exception Handling Summary

| Exception Type | Immediate Action | Escalation |
|---|---|---|
| Seal mismatch | Halt unloading, log REC-EX-01 | Warehouse Manager |
| Quantity discrepancy > 2% | Recount, log REC-EX-01 | Procurement |
| Physical damage | Segregate to DHA, photograph | Supplier Quality within 24h |
| Failed quality spot-check | Quality Hold tag applied | Procurement + Supplier Quality within 2h |

## Key Performance Targets
- Dock-to-putaway cycle time: under 3 hours for ambient goods, under 1 hour for temperature-controlled goods.
- Receiving accuracy: 99.5% GRN-to-physical-count match rate, measured monthly.

## Related Documents
- POL-PROC-001: Procurement Policy
- POL-QA-004: Quality Control Checklist — Incoming Goods
- SOP-WH-OUT-002: Warehouse Outbound Shipping SOP
