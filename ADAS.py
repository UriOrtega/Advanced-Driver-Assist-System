import cv2.cv2 as cv
import laneDetect as ld
import car_detect as cd
import processing as pro

width_of_lanes = 500
width_of_lanes2 = 500

net = pro.train_obj_detect()


def set_lines(number):
    global width_of_lanes
    global width_of_lanes2
    if number < 960:
        width_of_lanes = number
    else:
        width_of_lanes2 = number

def ADAS_sys(vid_file='Videos/solidWhiteRight.mp4'):
    global net, width_of_lanes,width_of_lanes2
    capture = cv.VideoCapture(vid_file)

    capture.set(3, 1920)
    capture.set(4, 1080)

    while True:
        isTrue, frame = capture.read()
        frame = cv.resize(frame, (1920, 1080))
        obj_detect = cd.object_detection(frame, net)
        final_product= ld.lane_detections(obj_detect, width_of_lanes, width_of_lanes2)


        yield final_product


# frames = ADAS_sys()
# #
# #
# # capture = cv.VideoCapture('Videos/Drive.mp4')
# # while True:
# #     isTrue, frame = capture.read()
# for frame in frames:
#     frame = cv.resize(frame, (1920, 1080))
#     finalLaneDetect = ld.lane_detections(frame, width_of_lanes, width_of_lanes2)
#     obj_detect = cd.object_detection(finalLaneDetect, net)
#
#     cv.imshow('Grame', obj_detect)
#
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break
#
# cv.destroyAllwindows()
