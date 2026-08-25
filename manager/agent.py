from google.adk.agents.llm_agent import Agent

from .sub_agents.stock_agent.agent import stock_agent


root_agent = Agent(
    name="manager",

    model="gemini-3.1-flash-lite",

    description="Main manager agent for StockPilot",

    instruction="""
    You are the Manager Agent for StockPilot.

    Your main responsibility is to understand the user's
    request and delegate work to the correct specialist agent.

    You oversee specialized agents.

    Available agents:

    STOCK AGENT

    Delegate tasks related to:

    - inventory
    - products
    - stock levels
    - low-stock products
    - reorder levels
    - purchase order requests

    to the stock_agent.

    Do not perform specialist inventory operations yourself.

    Always delegate stock-related tasks to stock_agent.
    """,

    sub_agents=[
        stock_agent
    ],
)