from playsound import playsound
import cv2.cv2 as cv
import car_functions as car


def alert_driver(img):
    cv.rectangle(img, (int((img.shape[1] / 2) - 100), int(img.shape[0] - 50)),
                 (int((img.shape[1] / 2) + 100), int(img.shape[0])), color=(0, 0, 255), thickness=-1)
    cv.rectangle(img, (int((img.shape[1] / 2) - 95), int(img.shape[0] - 45)),
                 (int((img.shape[1] / 2) + 95), int(img.shape[0]) - 5), color=(255, 255, 255), thickness=2)
    cv.putText(img, 'BRAKE', (int(img.shape[1] / 2) - 50, int(img.shape[0] - 15)), cv.FONT_HERSHEY_COMPLEX, 1,
               (255, 255, 255))

    playsound('Sound/car-beeping-2.mp3', False)
    display_warning()
    car.brake()
    return img


def display_warning():
    # print("STOP AHEAD!")
    pass
