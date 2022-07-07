import cv2
import car_functions as car


def train_obj_detect():
    configPath = 'ImgModelData/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'

    weightsPath = 'ImgModelData/frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    return net


def self_position(img, left, right):
    if left > 0 and right > 0:
        middle = int(img.shape[1] / 2)

        midpoint_of_lanes = int((left + right) / 2)

        if midpoint_of_lanes < middle:
            car.steer_right()

        if midpoint_of_lanes > middle:
            car.steer_left()

        if midpoint_of_lanes == middle:
            print('centered')
