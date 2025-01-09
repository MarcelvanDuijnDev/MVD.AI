import os
import json
import base64
import requests
from datetime import datetime

# Stable Diffusion WebUI server URL
WEBUI_SERVER_URL = 'http://127.0.0.1:7860'

# Output directories
OUT_DIR = 'api_out'
OUT_DIR_T2I = os.path.join(OUT_DIR, 'txt2img')
OUT_DIR_I2I = os.path.join(OUT_DIR, 'img2img')
os.makedirs(OUT_DIR_T2I, exist_ok=True)
os.makedirs(OUT_DIR_I2I, exist_ok=True)

def timestamp():
    """Generate a timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def encode_file_to_base64(path):
    """Convert an image file to a Base64 string."""
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def decode_and_save_base64(base64_str, save_path):
    """Decode a Base64 string and save it as an image."""
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

def call_api(api_endpoint, **payload):
    """Send a request to the Stable Diffusion WebUI API."""
    url = f"{WEBUI_SERVER_URL}/{api_endpoint}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def generate_txt2img(prompt, width=512, height=512, steps=20, cfg_scale=7, sampler="Euler a"):
    """Generate an image from text (txt2img)."""
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler,
    }
    response = call_api("sdapi/v1/txt2img", **payload)
    images = response.get("images", [])
    output_files = []

    # Decode and save each image
    for index, img in enumerate(images):
        save_path = os.path.join(OUT_DIR_T2I, f"txt2img-{timestamp()}-{index}.png")
        decode_and_save_base64(img, save_path)
        output_files.append(f"/generated_images/txt2img/{os.path.basename(save_path)}")

    return output_files

def generate_img2img(init_image_path, prompt, denoising_strength=0.5, width=512, height=512, steps=20):
    """Generate an image from another image (img2img)."""
    init_image = encode_file_to_base64(init_image_path)
    payload = {
        "prompt": prompt,
        "init_images": [init_image],
        "denoising_strength": denoising_strength,
        "width": width,
        "height": height,
        "steps": steps,
    }
    response = call_api("sdapi/v1/img2img", **payload)
    images = response.get("images", [])
    output_files = []
    for index, img in enumerate(images):
        save_path = os.path.join(OUT_DIR_I2I, f"img2img-{timestamp()}-{index}.png")
        decode_and_save_base64(img, save_path)
        output_files.append(save_path)
    return output_files
