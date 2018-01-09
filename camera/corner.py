import cv2
import numpy as np
from sklearn.cluster import KMeans


def prep_image(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    return gray

def detect_corners(image):
    # TODO: Tune the cornerHarris params
    dst = cv2.cornerHarris(image,2,3,0.04) # image, blockSize, kernel size, k

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    return dst

def classify_corners(image):
    white_pixels = np.argwhere(image > 0.01)

    kmeans = KMeans(n_clusters = 4).fit(white_pixels)

    corners = kmeans.cluster_centers_

    print(corners)

    TR = np.amax(corners, axis = 0)
    BL = np.amin(corners, axis = 0)

    print(TR)
    print(BL)

def main(image):
    log_file = open("log.txt", "w")

    prepped_image = prep_image(image)
    corners = detect_corners(prepped_image)
    corner_coords = classify_corners(corners)

    log_file.close()

    # for i, row in enumerate(corners):
        # for j, pixel in enumerate(row):
            # if pixel > 0.01:
                # print(i, j)
                # log_file.write(str(i) + ' ' + str(j) + '\n')

    # cv2.imshow('Image Title Goes Here', corners)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # filename = 'images/image0.jpg'
    # filename = 'chessboard.jpg'
    filename = 'simple.jpg'
    image = cv2.imread(filename)
    main(image)
