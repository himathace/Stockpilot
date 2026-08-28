from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

from ...tools.inventory import (
    get_inventory,
    get_low_stock,
)

from ...tools.orders import (
    create_reorder_request,
    approve_order

)


stock_agent = Agent(
    name="stock_agent",

    model="gemini-3.1-flash-lite",

    description="""
    Stock management specialist responsible for inventory,
    stock levels, low-stock detection and reorder requests.
    """,

    instruction="""
    You are the Stock Management Agent for StockPilot.

    You are responsible only for inventory and stock-related tasks.

    Your responsibilities include:

    - retrieving inventory information
    - checking current stock
    - identifying low-stock products
    - preparing reorder requests
    - explaining inventory information

    LOW STOCK RULE:

    A product is low stock when:

        current_stock < reorder_threshold

    When you identify a product that needs reordering,
    you may create a reorder request.

    The reorder request must remain:

        pending_approval

    IMPORTANT:

    You must NEVER claim that a purchase order has been placed
    before human approval.


    Actual order placement is handled separately after a human
    explicitly approves the order.
    """,

    tools=[
        get_inventory,
        get_low_stock,
        create_reorder_request,
        FunctionTool(approve_order, require_confirmation=True)

    ],
)