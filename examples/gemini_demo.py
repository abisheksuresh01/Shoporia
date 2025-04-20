import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def main():
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Define a system prompt
    system_prompt = """You are a helpful e-commerce customer service agent. 
    Your role is to assist customers with their inquiries about orders, products, 
    returns, and general questions. Be professional, friendly, and concise in your responses."""
    
    # Example customer message
    customer_message = "I ordered a product last week but haven't received it yet. Can you help me track my order?"
    
    # Create the full prompt
    prompt = f"{system_prompt}\n\nCustomer message: {customer_message}"
    
    # Generate response
    response = model.generate_content(prompt)
    
    # Print the response
    print("Customer: I ordered a product last week but haven't received it yet. Can you help me track my order?")
    print(f"Agent: {response.text}")
    
    # Example with conversation history
    print("\n--- With Conversation History ---\n")
    
    # Define conversation history
    history = [
        {"content": "Hello, I need help with my order", "is_from_user": True},
        {"content": "Hello! I'd be happy to help you with your order. Could you please provide your order number?", "is_from_user": False},
        {"content": "My order number is #12345", "is_from_user": True}
    ]
    
    # Format conversation history
    history_text = "\n".join([
        f"{'Customer' if msg['is_from_user'] else 'Agent'}: {msg['content']}"
        for msg in history
    ])
    
    # Create the full prompt with history
    full_prompt = f"{system_prompt}\n\nCurrent conversation context:\n{history_text}\n\nCustomer message: {customer_message}"
    
    # Generate response
    response = model.generate_content(full_prompt)
    
    # Print the response
    print("Customer: I ordered a product last week but haven't received it yet. Can you help me track my order?")
    print(f"Agent: {response.text}")

if __name__ == "__main__":
    main() 