import google.generativeai as genai
from app.core.config import settings
import json
from typing import Dict, List, Optional

def configure_gemini():
    """Configure the Gemini API with the API key"""
    genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_model(model_name: str = "gemini-2.0-flash"):
    """Get a Gemini model instance"""
    return genai.GenerativeModel(model_name)

def format_conversation_history(history: List[Dict]) -> str:
    """Format conversation history for the prompt"""
    return "\n".join([
        f"{'Customer' if msg['is_from_user'] else 'Agent'}: {msg['content']}"
        for msg in history[-5:]  # Last 5 messages for context
    ])

def format_prompt_for_json(base_prompt: str, conversation_history: Optional[List[Dict]] = None) -> str:
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
        history_text = format_conversation_history(conversation_history)
        return f"{base_prompt}\n\nCurrent conversation context:\n{history_text}\n{json_instructions}"
    
    return f"{base_prompt}\n{json_instructions}"

def parse_gemini_response(response_text: str) -> Dict:
    """Parse the Gemini response into a structured format"""
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

def generate_structured_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    model_name: str = "gemini-2.0-flash"
) -> Dict:
    """
    Generate a structured response from Gemini
    
    Args:
        prompt: The system prompt or base prompt
        conversation_history: Optional conversation history
        model_name: The Gemini model to use
        
    Returns:
        A structured response dictionary
    """
    # Configure Gemini
    configure_gemini()
    
    # Get the model
    model = get_gemini_model(model_name)
    
    # Format the prompt with JSON instructions
    full_prompt = format_prompt_for_json(prompt, conversation_history)
    
    # Generate response
    response = model.generate_content(full_prompt)
    
    # Parse and return the response
    return parse_gemini_response(response.text) 