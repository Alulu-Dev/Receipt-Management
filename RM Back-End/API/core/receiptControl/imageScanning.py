from tempfile import TemporaryDirectory

import cv2
import numpy as np
import pytesseract
# from pytesseract import Output
# from PIL import Image, ImageEnhance, ImageFilter

from API.core.receiptControl.imageUploading import upload_image_to_drive


# get grayscale image
def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# draw rectangle around texts
def bound_texts(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    return img


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


def scanner(file, filename, mimetype):
    image = cv2.imread(file)

    # grayscale result
    img = get_grayscale(image)
    img = remove_noise(img)

    # thresholding result
    img2 = thresholding(img)

    # erosion and dilate
    img3 = erode(image)
    img6 = remove_noise(get_grayscale(img3))
    img7 = erode(img2)
    img4 = dilate(img3)
    # opening
    img5 = opening(img4)

    # box texts
    # img4 = bound_texts(image)
    #
    with TemporaryDirectory(prefix='image') as tempdir:
        # im = pillow_trail(file)
        # im.save(tempdir + '/' + filename)
        # file_path = tempdir + "/" + filename
        #
        # text = pytesseract.image_to_string(file_path)
        # return "{}".format(text)
        cv2.imwrite(tempdir + "/" + filename, img)
        file_path1 = tempdir + "/" + filename

        text = pytesseract.image_to_string(file_path1)
        return "{}".format(text)
        # img4 = bound_texts(cv2.imread(file_path1))
        # # img4 = bound_texts(file_path1)
        # cv2.imwrite(tempdir + "/" + filename, img4)
        # file_path = tempdir + "/" + filename

        return upload_image_to_drive('AluluSuperAdmin', 0x6231c3773b3e717238f04daa, file_path, mimetype)
