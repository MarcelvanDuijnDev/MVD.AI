import anthropic
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize the Claude client
client = anthropic.Client(api_key=os.getenv("CLAUDE_AI_API_KEY"))

def process_claude_request(user_input):
    """Send a request to Claude AI and get the response."""
    if not user_input or not isinstance(user_input, str):
        return {"error": "Input message cannot be empty or invalid."}

    user_input = user_input.strip()

    try:
        # Create a Claude chat request
        response = client.completions.create(
            model="claude-2",
            prompt=f"{anthropic.HUMAN_PROMPT} {user_input}{anthropic.AI_PROMPT}",
            max_tokens_to_sample=200,
            temperature=0.7,
        )

        # Extract the completion text
        reply = response.completion if hasattr(response, "completion") else "No response received."
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
