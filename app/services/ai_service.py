from app.core.config import settings
from app.utils.gemini_utils import generate_structured_response
from typing import List, Dict
import random
import string

class AIService:
    def __init__(self):
        # Define the system prompt
        self.system_prompt = """You are a helpful e-commerce customer service agent. 
        Your role is to assist customers with their inquiries about orders, products, 
        returns, and general questions. Be professional, friendly, and concise in your responses.
        
        Available actions:
        - Check order status
        - Look up product information
        - Process returns
        - Cancel order
        - Place order
        - Answer general questions
        
        For order cancellation, you need the order number.
        For order placement, you need the product name, quantity, and shipping address.
        For cash on delivery, the order total must be under $100.
        
        Respond in JSON format with the following structure:
        {
            "response": "Your response to the customer",
            "action_needed": "action_type or null",
            "action_data": {} or null
        }"""
    
    async def process_message(self, message: str, conversation_history: List[Dict]) -> Dict:
        """
        Process a customer message and generate an appropriate response
        """
        try:
            # Create the full prompt with the customer message
            full_prompt = f"{self.system_prompt}\n\nCustomer message: {message}"
            
            # Generate response using the utility function
            return generate_structured_response(
                prompt=full_prompt,
                conversation_history=conversation_history,
                model_name="gemini-2.0-flash"  # Use Gemini 2.0 Flash model
            )
            
        except Exception as e:
            return {
                "response": "I apologize, but I'm having trouble processing your request. Please try again or contact human support.",
                "action_needed": None,
                "action_data": None
            }
    
    async def get_product_info(self, product_id: int) -> Dict:
        """
        Retrieve product information
        """
        # This would typically query your database
        # For now, returning a mock response
        return {
            "id": product_id,
            "name": "Sample Product",
            "description": "This is a sample product description",
            "price": 99.99,
            "stock": 100
        }
    
    async def check_order_status(self, order_number: str) -> Dict:
        """
        Check the status of an order
        """
        # This would typically query your database
        # For now, returning a mock response
        return {
            "order_number": order_number,
            "status": "Processing",
            "estimated_delivery": "2024-01-01"
        }
    
    def generate_order_number(self) -> str:
        """
        Generate a unique order number
        """
        # Generate a random 8-character alphanumeric string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(8)) 