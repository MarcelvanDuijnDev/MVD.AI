import mss
from PIL import Image
import io
import pytesseract

from dotenv import load_dotenv
import os
load_dotenv()

# Configure Tesseract (update the path if needed)
pytesseract.pytesseract.tesseract_cmd = os.getenv("PYTESSERACTPATH")

def capture_screen():
    """
    Capture the current screen and return the image as bytes.
    Returns:
        bytes: PNG image in bytes.
    """
    with mss.mss() as sct:
        # Capture the primary monitor
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Convert to bytes
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="PNG")
        img_byte_array.seek(0)
        return img_byte_array.getvalue()

def extract_text_from_image(image_bytes):
    """
    Extract text from an image in bytes format.
    Args:
        image_bytes (bytes): PNG image in bytes.
    Returns:
        str: Extracted text.
    """
    try:
        # Convert bytes back to an image
        img = Image.open(io.BytesIO(image_bytes))
        # Extract text
        extracted_text = pytesseract.image_to_string(img)
        return extracted_text.strip()
    except Exception as e:
        return f"Error: {e}"
