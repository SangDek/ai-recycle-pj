# views/views.py
from flask import Blueprint, render_template, Response
import cv2
from models.model import predict

views = Blueprint('views', __name__)

# Set up the camera
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Preprocess the frame
        img = cv2.resize(frame, (150, 150))
        img = np.expand_dims(img, axis=0)

        # Predict
        prob = predict(img)

        # Label the frame
        if prob > 0.5:
            label = f'Styrofoam: {prob:.2f}'
            color = (0, 255, 0)  # Green
        else:
            label = f'Not Styrofoam: {1 - prob:.2f}'
            color = (0, 0, 255)  # Red

        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Encode the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@views.route('/')
def index():
    return render_template('index.html', title='재활용품 분리수거 시스템')

@views.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
