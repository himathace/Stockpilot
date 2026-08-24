from google.adk.agents.llm_agent import Agent
from .tools.inventory import details

root_agent = Agent(
    name="manager",
    model="gemini-3.1-flash-lite",
    description="manager agent",
    instruction="""
    you are a manager agent that is responsible for overseeing the work of the other agents

    always delegate the task to the appropriate agent use your best judgment to determine which agent to delegate to 

    you are responsible for delegating tasks to the following agent
    - 
    -
    
    you also have access to following tools
    """,
    tools=[details],
)