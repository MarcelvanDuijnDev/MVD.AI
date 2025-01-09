from flask import Flask, Response, jsonify, request, render_template, send_from_directory, send_file
import threading
import time
import logging
import requests
import os
from modules.openai import process_openai_request
from modules.googleai import process_googleai_request
from modules.claude import process_claude_request
from modules.filter_manager import manage_filters
from modules.screencap_and_pytesseract import capture_screen, extract_text_from_image
from modules.activity_tracker import get_current_state
from modules.system_monitor import get_system_info
from modules.log_manager import read_logs, clear_logs
from modules.stable_diffusion import generate_txt2img, generate_img2img
from modules.azure_speech import synthesize_text_to_speech, recognize_speech_from_audio

app = Flask(__name__)

# Configure logging for the command window
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/openai_request', methods=['POST'])
def openai_request():
    """Handle OpenAI requests."""
    data = request.json
    logging.info(f"OpenAI Request received: {data}")
    response = process_openai_request(data)
    logging.info(f"OpenAI Response: {response}")
    return jsonify(response)

@app.route('/api/googleai_request', methods=['POST'])
def googleai_request():
    """Handle Google AI requests."""
    data = request.json
    logging.info(f"Google AI Request received: {data}")
    response = process_googleai_request(data)
    logging.info(f"Google AI Response: {response}")
    return jsonify(response)

@app.route('/api/claude_request', methods=['POST'])
def claude_request():
    """Handle Claude AI requests."""
    data = request.json
    user_input = data.get("input", "")  # Use "input" since the web interface sends this key
    logging.info(f"Claude AI Request received: {data}")
    response = process_claude_request(user_input)
    logging.info(f"Claude AI Response: {response}")
    return jsonify(response)

@app.route('/api/filters', methods=['GET', 'POST'])
def filters():
    """
    Manage filters via API.
    GET: View filters.
    POST: Update filters.
    """
    if request.method == 'POST':
        update_data = request.json
        logging.info(f"Updating filters: {update_data}")
        return jsonify(manage_filters(update_data))
    return jsonify(manage_filters())

@app.route('/api/logs/<log_type>', methods=['GET', 'POST'])
def logs(log_type):
    """
    Manage logs via API.
    GET: Read logs.
    POST: Clear logs.
    """
    if request.method == 'POST':
        logging.info(f"Clearing logs: {log_type}")
        return jsonify(clear_logs(log_type))
    logging.info(f"Fetching logs: {log_type}")
    return jsonify({"logs": read_logs(log_type)})

@app.route('/screenshot', methods=['GET'])
def serve_screenshot():
    """
    Serve a live screenshot as a PNG image.
    """
    try:
        image_bytes = capture_screen()
        return Response(image_bytes, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/extracted_text', methods=['GET'])
def serve_extracted_text():
    """
    Extract text from the current live screenshot.
    """
    try:
        image_bytes = capture_screen()
        extracted_text = extract_text_from_image(image_bytes)
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/state', methods=['GET'])
def state():
    """Fetch current activity tracker state via API."""
    response = get_current_state()
    logging.info(f"Activity Tracker State: {response}")
    return jsonify(response)

@app.route('/api/system_monitor', methods=['GET'])
def system_monitor():
    """
    Fetch system monitoring information.
    """
    response = get_system_info()
    logging.info(f"System Monitor: {response}")
    return jsonify(response)

@app.route('/api/activity_tracker', methods=['GET'])
def activity_tracker():
    """
    Fetch the current system activity tracker state.
    """
    response = get_current_state()
    logging.info(f"Activity Tracker State: {response}")
    return jsonify(response)

@app.route('/set_source', methods=['POST'])
def set_video_source():
    """Proxy source selection to live_object_detection.py."""
    data = request.json
    response = requests.post("http://127.0.0.1:5001/set_source", json=data)
    return jsonify(response.json())

@app.route('/live_feed')
def live_feed():
    """Proxy the live feed from live_object_detection.py."""
    try:
        response = requests.get("http://127.0.0.1:5001/live_feed", stream=True)
        return Response(response.iter_content(chunk_size=1024),
                        content_type=response.headers.get('Content-Type'))
    except Exception as e:
        app.logger.error(f"Error fetching live feed: {e}")
        return jsonify({"error": "Unable to fetch live feed"}), 500

@app.route('/api/stable_diffusion/txt2img', methods=['POST'])
def txt2img():
    """Generate an image from text."""
    data = request.json
    prompt = data.get("prompt", "")
    width = data.get("width", 512)
    height = data.get("height", 512)
    steps = data.get("steps", 20)
    cfg_scale = data.get("cfg_scale", 7)
    sampler = data.get("sampler", "Euler a")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        output_files = generate_txt2img(prompt, width, height, steps, cfg_scale, sampler)
        return jsonify({"generated_images": output_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stable_diffusion/img2img', methods=['POST'])
def img2img():
    """Generate an image from another image."""
    data = request.json
    init_image_path = data.get("init_image_path", "")
    prompt = data.get("prompt", "")
    denoising_strength = data.get("denoising_strength", 0.5)
    width = data.get("width", 512)
    height = data.get("height", 512)
    steps = data.get("steps", 20)
    
    if not (prompt and init_image_path):
        return jsonify({"error": "Prompt and init_image_path are required"}), 400

    try:
        output_files = generate_img2img(init_image_path, prompt, denoising_strength, width, height, steps)
        return jsonify({"generated_images": output_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generated_images/txt2img/<filename>')
def serve_txt2img(filename):
    return send_from_directory('api_out/txt2img', filename)

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """Endpoint for text-to-speech conversion."""
    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'en-US-AriaNeural')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = synthesize_text_to_speech(text, voice_name=voice)
    return jsonify(result)

@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    """Endpoint for speech-to-text transcription."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    save_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(save_path)

    result = recognize_speech_from_audio(save_path)

    # Clean up uploaded file
    os.remove(save_path)
    return jsonify(result)

@app.route('/static/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve generated audio files."""
    file_path = os.path.join("static", "audio", filename)
    try:
        return send_file(file_path, mimetype="audio/wav")
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
