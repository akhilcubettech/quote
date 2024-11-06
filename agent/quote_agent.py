from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from agent.llm_manager import LLMManager
from dotenv import load_dotenv
from products import products_
import time

load_dotenv()


class QuoteAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def fetch_db(self, state: dict):
        self.llm_manager = LLMManager()
        time.sleep(2)
        return {'products': products_}

    def generate_quote(self, state: dict):
        requirements = state['requirements']
        products = state['products']
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are an AI quote generator designed to create highly professional quotations based on a provided requirements and results information. 
           Analyze the requirements and products, identify any relevant information like price quantity etc, and use those to create a quote for the requirements.

           Your output should follow this exact JSON structure:
    [
    
    {{
        "product_id": str,    # ID of the product
        "product_name": str,  # Name of the product
        "product_price": 289.00, # Price of the product
        "quantity": int , # Quantity of product from requirements
        "sub_total: float, # Total Price per item (quantity * product_price)
    }},
    {{
        "product_id": str,    # ID of the product
        "product_name": str,  # Name of the product
        "product_price": 289.00, # Price of the product
        "quantity": int , # Quantity of product from requirements
        "sub_total: float, # Total Price per item (quantity * product_price)
    }}
    
    ]
    '''),
            ("human", "===Requirements:\n{requirements}\n\n===Results:\n{results}\n\nGenerate a list of items for quote:")])

        output_parser = JsonOutputParser()
        response = self.llm_manager.invoke(prompt, requirements=requirements, results=products )
        items = output_parser.parse(response)
        return {"items": items}
