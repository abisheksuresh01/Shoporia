import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def format_prompt_for_json(message):
    """Format the prompt to explicitly request JSON output"""
    return f"""You are a helpful e-commerce customer service agent. 
    Your role is to assist customers with their inquiries about orders, products, 
    returns, and general questions. Be professional, friendly, and concise in your responses.
    
    Available actions:
    - Check order status
    - Look up product information
    - Process returns
    - Answer general questions
    
    IMPORTANT: You MUST respond in valid JSON format with the following structure:
    {{
        "response": "Your response to the customer",
        "action_needed": "action_type or null",
        "action_data": {{}} or null
    }}
    
    Do not include any text outside of the JSON structure.
    
    Customer message: {message}"""

def parse_response(response_text):
    """Parse the response text into a structured format"""
    # Try to find JSON in the response
    try:
        # First attempt: try to parse the entire response as JSON
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Second attempt: try to find JSON within the response
        try:
            # Look for JSON-like structure
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # If all attempts fail, create a structured response
        return {
            "response": response_text,
            "action_needed": None,
            "action_data": None
        }

def main():
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Example customer messages
    messages = [
        "I ordered a product last week but haven't received it yet. Can you help me track my order?",
        "What's the status of my order #12345?",
        "I want to return the product I received yesterday. It's damaged.",
        "Do you have any information about the new iPhone model?"
    ]
    
    # Process each message
    for message in messages:
        print(f"\nCustomer: {message}")
        
        # Create the full prompt with explicit JSON formatting instructions
        prompt = format_prompt_for_json(message)
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Parse the response
        parsed_response = parse_response(response.text)
        
        # Print the structured response
        print(f"Agent: {parsed_response['response']}")
        if parsed_response['action_needed']:
            print(f"Action needed: {parsed_response['action_needed']}")
            print(f"Action data: {parsed_response['action_data']}")
        
        # Print the raw response for debugging
        print("\n--- Raw Response ---")
        print(response.text)
        print("-------------------")

if __name__ == "__main__":
    main() 