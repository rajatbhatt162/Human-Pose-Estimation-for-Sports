from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import os

app = Flask(__name__)

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to process image upload
@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    in_memory_file = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)
    
    # Pose estimation on the image
    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # Save the processed image
    processed_image_path = 'static/processed_image.jpg'
    cv2.imwrite(processed_image_path, img)
    return jsonify({'image_url': processed_image_path})

# Route to process video upload
@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    
    video_file = request.files['video']
    video_path = os.path.join('static', video_file.filename)
    video_file.save(video_path)
    
    # Process video for pose estimation
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    processed_video_path = 'static/processed_video.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(processed_video_path, fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Pose estimation on each frame
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        out.write(frame)
    
    cap.release()
    out.release()
    return jsonify({'video_url': processed_video_path})

# Route to capture pose from camera
@app.route('/process_camera', methods=['GET'])
def process_camera():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Pose estimation on each frame
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('Pose Estimation', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return jsonify({'status': 'Camera feed ended'})

if __name__ == '__main__':
    app.run(debug=True)
