import numpy as np
import cv2
import glob
import shutil


def prepro(filename, zone, prefix):
    oriimg = cv2.imread(filename)

    # keep the interesting part
    (a, b, c, d) = zone
    text_zone = oriimg[a:b, c:d]
    height, width, depth = text_zone.shape

    # resize it to be bigger (so less pixelized)
    end_height = 50
    img_scale = end_height / height
    new_x, new_y = text_zone.shape[1] * img_scale, text_zone.shape[0] * img_scale
    newimg = cv2.resize(text_zone, (int(new_x), int(new_y)))

    # binarize it
    gray = cv2.cvtColor(newimg, cv2.COLOR_BGR2GRAY)
    th, img = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

    # erode it
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(prefix+'_ero.png', erosion)

    cv2.imshow("Show by CV2", erosion)
    cv2.waitKey(0)


if __name__ == '__main__':
    img_path = "network_drive/"
    filelist = glob.glob(img_path + "*.jpg")
    for img in filelist:
        print(img)
        # prepro(img, (16, 27, 6, 130), 'up_line')
        # prepro(img, (27, 36, 6, 130), 'down_line')

