from flask import Flask, Response
import cv2 as cv

app = Flask(__name__)
camera = cv.VideoCapture(0)
print(camera)
print(camera.isOpened())

def gen_frames():
  while True:
    success, frame = camera.read()
    if not success:
      print("failed to fetch camera")
      break
    else:
      ret, buffer = cv.imencode('.jpg',frame)
      frame = buffer.tobytes()
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)