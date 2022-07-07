import alert_driver


def distance_measurement(img, x, w, y, h):
    if x < img.shape[1] / 2 < (x + w) and y > img.shape[0] / 2 < (y + h):
        img = alert_driver.alert_driver(img)
