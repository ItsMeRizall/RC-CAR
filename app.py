from flask import Flask, render_template, Response, request
import cv2
from ultralytics import YOLO
import supervision as sv
import motor_control as motor
import time

app = Flask(__name__)

# Load model & camera
camera = cv2.VideoCapture(0)
model = YOLO('best.pt')  # Ganti dengan path model Anda
tracker = sv.ByteTrack()

# Ambil nama kelas dari model
class_names = list(model.names.values())  # Otomatis dari model
print("\n[INFO] Loaded class names from model:")
for idx, name in enumerate(class_names):
    print(f"  {idx}: {name}")

# Tambahan: tampilkan dict model.names mentah
print("\n[DEBUG] model.names dict:", model.names)

# Target class berbasis nama
target_name = 'cat'  # default
last_action_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_target_name')
def set_target_name():
    global target_name
    target_name = request.args.get('name')
    print(f"\n[TARGET SET] New target name: {target_name}")
    return ('', 204)

def gen_frames():
    global last_action_time

    frame_count = 0
    while True:
        frame_count += 1
        success, frame = camera.read()
        if not success:
            print("[ERROR] Failed to read frame from camera.")
            break

        print(f"\n--- Frame {frame_count} ---")

        results = model(frame, conf=0.5)
        detections = sv.Detections.from_ultralytics(results[0])
        tracks = tracker.update_with_detections(detections)

        print(f"[INFO] Detections: {len(detections)} | Tracks: {len(tracks)}")
        for i in range(len(detections)):
            box = detections.xyxy[i]
            cls = detections.class_id[i]
            print(f"[ALL DETECTIONS] box={box}, class_id={cls}")

        followed = None

        if len(tracks) == 0:
            motor.stop()
            print("[INFO] No objects detected. Motor stopped.")
        else:
            for i, track in enumerate(tracks):
                try:
                    xyxy = track[0]
                    class_id = int(track[3])
                    x1, y1, x2, y2 = map(float, xyxy)

                    if class_id < 0 or class_id >= len(class_names):
                        print(f"[SKIP] Invalid class_id: {class_id}. Total classes: {len(class_names)}")
                        continue

                    name = class_names[class_id]
                    print(f"[TRACK {i}] Found: {name} (class_id={class_id}) | Target: {target_name}")

                    if name == target_name:
                        followed = (x1, y1, x2, y2)
                        print(f"[FOLLOWING] MATCHED {name} at xyxy={followed}")
                        break
                except Exception as e:
                    print(f"[ERROR] While parsing track: {e}")
                    continue



        if not followed:
            motor.stop()
            print("[WARNING] No target match. Motor stopped.")
        else:
            now = time.time()
            if now - last_action_time > 0.3:
                x1, y1, x2, y2 = followed
                x_center = (x1 + x2) / 2
                frame_width = frame.shape[1]

                if x_center < frame_width * 0.4:
                    motor.left()
                    print("➡️ Motor: LEFT")
                elif x_center > frame_width * 0.6:
                    motor.right()
                    print("⬅️ Motor: RIGHT")
                else:
                    motor.forward()
                    print("⬆️ Motor: FORWARD")

                last_action_time = now

        # Visualisasi hasil
        annotated = results[0].plot()
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    motor.stop()
    return ('', 204)

@app.route('/cleanup')
def cleanup():
    motor.cleanup()
    return ('Cleaned up', 200)

if __name__ == '__main__':
    try:
        print("[STARTING] Flask app running at http://localhost:5000")
        app.run(host='0.0.0.0', port=5000)
    finally:
        motor.cleanup()
