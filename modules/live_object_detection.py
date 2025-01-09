import cv2
import numpy as np
from flask import Flask, Response, request
import mss
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
model = YOLO('models/yolov5s.pt')  # Pre-trained YOLOv5 small model

# Video source management
video_capture = None
current_source = "webcam"


def set_source(source):
    """Change the video source dynamically."""
    global video_capture, current_source
    current_source = source

    # Release the previous capture
    if video_capture:
        video_capture.release()

    # Webcam source
    if source == "webcam":
        video_capture = cv2.VideoCapture(0)
    elif source == "screencapture":
        video_capture = None  # Screen capture doesn't use VideoCapture


def capture_screen():
    """Capture the screen using mss."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        image = np.array(screenshot)
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)


def generate_frames():
    """Generate video frames with YOLO object detection."""
    while True:
        if current_source == "webcam" and video_capture:
            success, frame = video_capture.read()
            if not success:
                break
        elif current_source == "screencapture":
            frame = capture_screen()

        # Perform YOLO object detection
        results = model(frame)

        # Annotate the frame with bounding boxes and labels
        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            confidence = result.conf[0]
            label = result.cls[0]
            label_name = model.names[int(label)]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label_name} ({confidence:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/live_feed')
def live_feed():
    """Serve the processed video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/set_source', methods=['POST'])
def set_video_source():
    """Change the video source."""
    data = request.json
    source = data.get("source")
    if source in ["webcam", "screencapture"]:
        set_source(source)
        return {"status": "success", "source": source}, 200
    return {"status": "error", "message": "Invalid source"}, 400


if __name__ == '__main__':
    set_source("webcam")  # Default source
    app.run(host='127.0.0.1', port=5001)
