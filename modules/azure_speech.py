import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
load_dotenv()

# Set up Azure credentials
API_KEY = os.getenv("AZURE_API_KEY")
REGION = os.getenv("AZURE_REGION")

def synthesize_text_to_speech(text, output_file="output.wav", voice_name="en-US-AriaNeural"):
    """Convert text to speech and save it as an audio file."""
    try:
        # Define the correct output directory and file
        output_folder = os.path.join("static", "audio")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "output.wav")

        print(f"Saving audio to: {output_file}")

        # Create a speech config
        speech_config = speechsdk.SpeechConfig(subscription=API_KEY, region=REGION)
        speech_config.speech_synthesis_voice_name = voice_name

        # Configure the audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

        # Create the speech synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Perform the synthesis
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized successfully. File saved to {output_file}.")
            return {"success": True, "file_url": f"/static/audio/{os.path.basename(output_file)}"}
        else:
            return {"success": False, "error": str(result.cancellation_details)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def recognize_speech_from_audio(audio_file):
    """Convert speech to text from an audio file."""
    try:
        # Create a speech config
        speech_config = speechsdk.SpeechConfig(subscription=API_KEY, region=REGION)

        # Configure the audio input
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

        # Create the speech recognizer
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Perform recognition
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized text: {result.text}")
            return {"success": True, "transcription": result.text}
        else:
            return {"success": False, "error": str(result.cancellation_details)}
    except Exception as e:
        return {"success": False, "error": str(e)}
