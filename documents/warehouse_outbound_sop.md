---
doc_id: SOP-WH-OUT-002
title: Warehouse Outbound Shipping — Standard Operating Procedure
category: sop
department: Warehouse Operations
version: 1.6
status: active
effective_date: 2025-08-15
last_reviewed: 2025-12-10
owner: Warehouse Operations Manager
---

# ABC Corporation — Warehouse Outbound Shipping SOP

## Purpose
To standardize order picking, packing, and dispatch procedures across ABC distribution centers, ensuring order accuracy and on-time carrier pickup.

## Procedure

**1. Order Release**
Orders are released from the order management system (OMS) to the WMS in wave batches. Standard wave cutoff is 2:00 PM local time for next-day carrier pickup; expedited orders may be released ad hoc with Shift Supervisor approval.

**2. Picking**
- Pickers follow system-directed pick paths (zone-based picking for DC-01 through DC-04; batch picking for DC-05 through DC-07).
- Barcode scan required at each pick to confirm SKU and quantity.
- Short picks (inventory shown as available but not physically found) must be logged as a Short Pick Exception and trigger an immediate cycle count of that bin location.

**3. Packing**
- Pack stations verify picked items against the pick list before sealing.
- Fragile or hazardous items follow packaging guidelines in Appendix A (see facility-specific packing manual).
- Packing slip and shipping label generated simultaneously; mismatched label/slip pairs must not be shipped.

**4. Staging and Load Verification**
- Packed orders staged by carrier and route.
- Load verification: outbound piece count must match manifest before trailer seal is applied.
- Seal number recorded in WMS and communicated to the carrier's dispatch system where EDI integration exists.

**5. Dispatch**
- Trailer departs only after Bill of Lading (BOL) is signed by both warehouse staff and carrier driver.
- BOL copy retained on-site for 90 days minimum; digital copy archived indefinitely.

## Order Accuracy Standards
- Target pick accuracy: 99.7% (measured as order lines shipped correctly / total order lines).
- Any shipment error affecting a customer order must be logged in the Customer Impact Log within 4 hours of discovery.

## Escalation Matrix

| Issue | Owner | Response Time |
|---|---|---|
| Short pick / inventory discrepancy | Shift Supervisor | Immediate cycle count |
| Carrier no-show | Transportation Coordinator | Rebook within 2 hours |
| Mislabeled shipment caught pre-dispatch | Pack Station Lead | Immediate correction, no escalation needed |
| Mislabeled shipment shipped | Warehouse Manager | Customer Impact Log + carrier recall attempt |

## Related Documents
- SOP-WH-IN-001: Warehouse Inbound Receiving SOP
- POL-PROC-001: Procurement Policy
