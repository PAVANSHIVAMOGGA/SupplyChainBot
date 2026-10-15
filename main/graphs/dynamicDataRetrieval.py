import requests
from langchain_core.tools import tool
from langgraph.types import interrupt

from supplyChainBot.main.graphs.liveDataAPIcall import liveDataApiGETCall, liveDataApiPOSTCall


@tool
def getInventoryDetails(sku: str):
    """Function to do a API call to track Inventory details"""
    url = f"http://127.0.0.1:8001/inventory/{sku}"

    return liveDataApiGETCall(url=url)


@tool
def getShipmentDetails(shipmentId: str):
    """Function to do a API call to track Shipment details"""
    url = f"http://127.0.0.1:8001/shipment/{shipmentId}"

    return liveDataApiGETCall(url=url)

@tool
def doSKUReorder(sku: str, quantity: int, idempotency_key: str):
    """Function to call the API to reorder the SKU if it's in stock"""
    is_appproved = interrupt(f"Order is being placed for {sku} with {quantity} units, Please review and approve with True/False")

    if (is_appproved):
        url = f"http://127.0.0.1:8001/inventory/{sku}/reorder"
        payload = {
            "quantity": quantity,
            "idempotency_key": idempotency_key
        }

        return liveDataApiPOSTCall(url=url, payload=payload)

    else:
        return "Your request was rejected by the approver"