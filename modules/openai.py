from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

def process_openai_request(data):
    """
    Process a request for OpenAI.
    Args:
        data (dict): Contains the user's input.
    Returns:
        dict: AI response or error message.
    """
    user_input = data.get("input", "")
    if not user_input.strip():
        return {"error": "No input provided"}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
