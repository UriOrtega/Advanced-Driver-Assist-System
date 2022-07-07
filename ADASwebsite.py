import ADAS
from flask import Response, Flask, render_template, request
import threading
import argparse
import cv2.cv2 as cv
import laneDetect as ld
import car_detect as cd
import processing as pro
import os

outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
width_of_lanes = 500
width_of_lanes2 = 500

net = pro.train_obj_detect()
capture = cv.VideoCapture('Videos/Drive.mp4')


@app.route("/")
def index():
    # return the rendered templates
    return render_template("index.html")


def out_frame():
    global outputFrame, lock
    global capture

    capture.set(3, 1920)
    capture.set(4, 1080)

    while True:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (1920, 1080))
        finalLaneDetect = ld.lane_detections(frame, width_of_lanes, width_of_lanes2)
        obj_detect = cd.object_detection(finalLaneDetect, net)

        ret, buffer = cv.imencode('.jpg', obj_detect)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(out_frame(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=out_frame())
    t.daemon = True
    t.start()
    # start the flask app
    app.run(debug=True, threaded=True, use_reloader=False)
