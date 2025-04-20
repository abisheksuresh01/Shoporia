import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def format_prompt_for_json(base_prompt, conversation_history=None):
    """Format the prompt to explicitly request JSON output"""
    # Add JSON formatting instructions to the prompt
    json_instructions = """
    IMPORTANT: You MUST respond in valid JSON format with the following structure:
    {
        "response": "Your response to the customer",
        "action_needed": "action_type or null",
        "action_data": {} or null
    }
    
    Do not include any text outside of the JSON structure.
    """
    
    # Add conversation history if provided
    if conversation_history:
        history_text = "\n".join([
            f"{'Customer' if msg['is_from_user'] else 'Agent'}: {msg['content']}"
            for msg in conversation_history
        ])
        return f"{base_prompt}\n\nCurrent conversation context:\n{history_text}\n{json_instructions}"
    
    return f"{base_prompt}\n{json_instructions}"

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
    
    # Define a system prompt
    system_prompt = """You are a helpful e-commerce customer service agent. 
    Your role is to assist customers with their inquiries about orders, products, 
    returns, and general questions. Be professional, friendly, and concise in your responses.
    
    Available actions:
    - Check order status
    - Look up product information
    - Process returns
    - Answer general questions"""
    
    # Initialize conversation history
    conversation_history = []
    
    # Example conversation flow
    customer_messages = [
        "Hello, I need help with my order",
        "My order number is #12345",
        "I ordered it last week but haven't received it yet",
        "Can you tell me when it will arrive?",
        "Thank you for your help"
    ]
    
    # Process each message in the conversation
    for message in customer_messages:
        print(f"\nCustomer: {message}")
        
        # Add customer message to history
        conversation_history.append({
            "content": message,
            "is_from_user": True
        })
        
        # Create the full prompt with JSON instructions
        prompt = format_prompt_for_json(system_prompt, conversation_history)
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Parse the response
        parsed_response = parse_response(response.text)
        agent_response = parsed_response['response']
        
        # Print the structured response
        print(f"Agent: {agent_response}")
        if parsed_response['action_needed']:
            print(f"Action needed: {parsed_response['action_needed']}")
            print(f"Action data: {parsed_response['action_data']}")
        
        # Add agent response to history
        conversation_history.append({
            "content": agent_response,
            "is_from_user": False
        })
        
        # Print the raw response for debugging
        print("\n--- Raw Response ---")
        print(response.text)
        print("-------------------")
    
    # Print the full conversation
    print("\n--- Full Conversation ---\n")
    for msg in conversation_history:
        role = "Customer" if msg['is_from_user'] else "Agent"
        print(f"{role}: {msg['content']}")

if __name__ == "__main__":
    main() 