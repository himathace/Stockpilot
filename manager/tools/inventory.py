from ..database import get_connection


def get_inventory():
    """
    Get all current inventory with product and supplier information.    
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.sku,
            p.name,
            p.category,
            p.cost_price,

            i.current_stock,
            i.reorder_threshold,
            i.reorder_qty,

            s.id AS supplier_id,
            s.name AS supplier_name,
            s.email AS supplier_email,
            s.lead_time_days

        FROM inventory i

        JOIN products p
            ON i.product_id = p.id

        JOIN suppliers s
            ON p.supplier_id = s.id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_low_stock():
    """
    Find all products where stock is below the reorder threshold.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id AS product_id,
            p.sku,
            p.name,
            p.cost_price,

            i.current_stock,
            i.reorder_threshold,
            i.reorder_qty,

            s.id AS supplier_id,
            s.name AS supplier_name,
            s.email AS supplier_email,
            s.lead_time_days

        FROM inventory i

        JOIN products p
            ON i.product_id = p.id

        JOIN suppliers s
            ON p.supplier_id = s.id

        WHERE i.current_stock < i.reorder_threshold
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]