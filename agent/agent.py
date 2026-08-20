from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name='agent',
    model='gemini-3.1-flash-lite',
    description="greeting agent",
    instruction="You are a helpful assistant that greets user ask users name and greet them by name",
)