import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

# Configure Google AI API Key
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def process_googleai_request(data):
    """
    Process a request for Google AI.
    Args:
        data (dict): Contains the user's input.
    Returns:
        dict: AI response or error message.
    """
    user_input = data.get("input", "")
    if not user_input.strip():
        return {"error": "No input provided"}

    try:
        """model = genai.GenerativeModel("chat-bison")
        response = model.generate_content(user_input)"""
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(user_input)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}
