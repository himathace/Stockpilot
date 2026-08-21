from firebase import db


def details():
    """
    Get the current inventory details from Firestore.

    Returns:
        A list of current inventory items.
    """

    docs = db.collection("inventory").stream()

    inventory = []

    for doc in docs:
        data = doc.to_dict()

        inventory.append({
            "sku": data.get("sku"),
            "name": data.get("name"),
            "current_stock": data.get("current_stock"),
            "reorder_threshold": data.get("reorder_threshold"),
            "reorder_qty": data.get("reorder_qty"),
            "unit_cost": data.get("unit_cost"),
            "supplier_name": data.get("supplier_name"),
            "supplier_email": data.get("supplier_email"),
            "status": data.get("status"),
        })

    return inventory