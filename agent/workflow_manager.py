import os
from agent.quote_agent import QuoteAgent
from langgraph.graph import StateGraph, END
from agent.state import State

LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT')


class WorkflowManager:
    def __init__(self):
        self.agent = QuoteAgent()

    def text_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(State)

        # nodes
        workflow.add_node("fetch_db", self.agent.fetch_db)
        workflow.add_node("generate_quote", self.agent.generate_quote)

        # edges
        workflow.add_edge("fetch_db", "generate_quote")
        workflow.add_edge("generate_quote", END)
        workflow.set_entry_point("fetch_db")

        return workflow



    def run_text(self, requirements: str) -> dict:
        """Run the agent workflow and return the formatted response."""
        app = self.text_workflow().compile()
        data = app.invoke({"requirements": requirements})
        return data
