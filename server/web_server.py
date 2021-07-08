from flask import Response
from flask import Flask, jsonify
from flask import render_template
import threading
import argparse
import cv2
from datetime import datetime
import imagezmq

from stream.source import OpencvSource

output_frame = None
lock = threading.Lock()

app = Flask(__name__)

src = OpencvSource(src=0, name="default", width=640, height=480)

# image_hub = imagezmq.ImageHub(open_port="tcp://127.0.0.1:5556")


def get_stream():
    global src, lock, output_frame

    while True:
        _, frame = src.read()

        with lock:
            output_frame = frame.copy()


def generate():
    global image_hub

    while True:
        # msg, frame = image_hub.recv_image()
        # image_hub.send_reply(b'Ok')

        with lock:
            if output_frame is None:
                continue

            flag, encoded_image = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_image) + b'\r\n')


@app.route("/")
def index():
    t_ = datetime.now()
    data = {"project": "Face Recognition",
            "time": t_.timestamp()}
    return jsonify(data)


@app.route("/api/stream/demo/")
def demo():
    return render_template("demo.html")


@app.route("/api/stream/default/")
def default_streamer():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


t = threading.Thread(target=get_stream, args=())
t.daemon = True
t.start()

app.run(host="127.0.0.1", port=8000, debug=True, threaded=True,use_reloader=False)
