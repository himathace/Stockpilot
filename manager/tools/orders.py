from ..database import get_connection

def create_reorder_request(product_id: int):
    """
    Create a pending purchase order for a low-stock product.

    Does not place the order.
    Human approval is required first.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Get product information
    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.name,
            p.cost_price,

            p.supplier_id,

            i.current_stock,
            i.reorder_threshold,
            i.reorder_qty

        FROM products p

        JOIN inventory i
            ON p.id = i.product_id

        WHERE p.id = ?
    """, (product_id,))

    product = cursor.fetchone()

    if product is None:
        conn.close()

        return {
            "success": False,
            "message": "Product not found"
        }

    # Check whether stock actually needs reordering
    if product["current_stock"] >= product["reorder_threshold"]:
        conn.close()

        return {
            "success": False,
            "message": "Product does not need reordering"
        }

    # Check for existing order
    cursor.execute("""
        SELECT id, status

        FROM purchase_orders

        WHERE product_id = ?

        AND status IN (
            'pending_approval',
            'approved',
            'ordered'
        )

        LIMIT 1
    """, (product_id,))

    existing_order = cursor.fetchone()

    if existing_order:
        conn.close()

        return {
            "success": False,
            "message": "An active reorder already exists",
            "order_id": existing_order["id"],
            "status": existing_order["status"]
        }

    quantity = product["reorder_qty"]

    unit_cost = product["cost_price"]

    total_cost = quantity * unit_cost

    cursor.execute("""
        INSERT INTO purchase_orders (
            product_id,
            supplier_id,
            quantity,
            unit_cost,
            total_cost,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product["product_id"],
        product["supplier_id"],
        quantity,
        unit_cost,
        total_cost,
        "pending_approval"
    ))

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Reorder request created",
        "order_id": order_id,
        "product": product["name"],
        "quantity": quantity,
        "total_cost": total_cost,
        "status": "pending_approval"
    }


def approve_order(order_id: int) -> dict:
    """Approve a pending purchase order."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM purchase_orders WHERE id = ?",
        (order_id,)
    )
    order = cursor.fetchone()

    if order is None:
        conn.close()
        return {
            "success": False,
            "message": "Order not found"
        }

    if order["status"] != "pending_approval":
        conn.close()
        return {
            "success": False,
            "message": f"Order cannot be approved. Current status: {order['status']}"
        }

    cursor.execute("""
        UPDATE purchase_orders
        SET
            status = 'approved',
            approved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (order_id,))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "order_id": order_id,
        "status": "approved"
    }



