from flask import Flask, render_template, Response, request
import cv2
import motor_control as motor

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['GET'])
def move():
    direction = request.args.get('dir')
    if direction == 'forward':
        motor.forward()
    elif direction == 'backward':
        motor.backward()
    elif direction == 'left':
        motor.left()
    elif direction == 'right':
        motor.right()
    else:
        motor.stop()
    return ('', 204)

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
        app.run(host='0.0.0.0', port=5000)
    finally:
        motor.cleanup()
