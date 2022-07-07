import cv2.cv2 as cv
import numpy as np
import processing


def canny_frame(video_frame):
    gray = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), 0)
    canny = cv.Canny(blur, 75, 130)

    return canny


def region_of_interest(video_frame, interest_width, interest_width2):
    height = video_frame.shape[0]
    width = video_frame.shape[1]

    blank = np.zeros((height, width), dtype='uint8')

    rectangle = cv.rectangle(blank.copy(), (interest_width, height - 200), (width - interest_width2, height - 400), 255,
                             -1)

    # widthin10 = int(width / 10)
    # triangle = np.array(
    #     [[(widthin10 , height - 100), (int(widthin10 * 8), height - 100), (int(width / 2), int(height / 1.4))]])
    # in_triangle = np.array([[(widthin10 + 200, height), (int(widthin10 * 8) - 200, height),
    #                           (int(width / 2), int(height / 1.4) - 20)]])

    mask = np.zeros_like(video_frame)
    mask = cv.bitwise_xor(rectangle, mask)

    # cv.fillPoly(mask, triangle, 255)
    # cv.fillPoly(mask, in_triangle, 0)
    masked_image = cv.bitwise_and(video_frame, mask)

    return masked_image


def make_average_line(image, line_params):
    slope, intercept = line_params

    y1 = image.shape[0] - 100
    y2 = int(image.shape[0] / 1.8)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    cv.line(image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return x1


# noinspection PyBroadException
def display_lines(frame_image, mask):
    lines = cv.HoughLinesP(mask, 2, np.pi / 180, 100, np.array([]), minLineLength=10, maxLineGap=30)
    line_image = np.zeros_like(frame_image)
    left_fit = []
    left_int = 0

    right_fit = []
    right_int = 0

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]

            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))

            else:
                right_fit.append((slope, intercept))

        try:
            left_fit_average = np.average(left_fit, axis=0)
            left_int = make_average_line(line_image, left_fit_average)
        except:
            pass

        try:
            right_fit_average = np.average(right_fit, axis=0)
            right_int = make_average_line(line_image, right_fit_average)
        except:
            pass

        processing.self_position(line_image, left_int, right_int)

    return line_image


def lane_detections(frame, w1, w2):
    lane_image = np.copy(frame)

    canny = canny_frame(lane_image)

    mask = region_of_interest(canny, w1, w2)

    line_image = display_lines(lane_image, mask)

    combo = cv.addWeighted(lane_image, 0.8, line_image, 1, 1)

    return combo
