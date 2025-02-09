from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
  
client = OpenAI(
api_key=os.getenv("GROK_API_KEY"),
base_url="https://api.x.ai/v1",
)

def process_grok_request(user_input):
    """Send a request to Grok and get the response."""
    if not user_input or not isinstance(user_input, str):
        return {"error": "Input message cannot be empty or invalid."}

    user_input = user_input.strip()

    try:
        # Create a Grok chat request
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        # Extract the completion text
        reply = response.choices[0].message.content if response.choices else "No response received."
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
