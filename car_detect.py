import cv2
import numpy as np
import radar


def object_detection(img, net):
    thresh = 0.6  # Threshold to detect object
    nms_threshold = 0.1
    classFile = 'ImgModelData/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    classIds, conf, bbox = net.detect(img, confThreshold=thresh)
    bbox = list(bbox)
    conf = list(np.array(conf).reshape(1, -1)[0])
    conf = list(map(float, conf))

    indices = cv2.dnn.NMSBoxes(bbox, conf, thresh, nms_threshold)

    for i in indices:
        ind = i
        box = bbox[ind]
        con = conf[ind]
        x, y, w, h = box[0], box[1], box[2], box[3]

        if 0 <= ind <= 13:
            cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
            cv2.putText(img, f'{classNames[classIds[ind] - 1].upper()} - {round(con, 2)}', (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            radar.distance_measurement(img, x, w, y, h)

    return img
