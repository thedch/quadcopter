import cv2
import numpy as np
from sklearn.cluster import KMeans


def prep_image(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    return gray

def detect_corners(image):
    dst = cv2.cornerHarris(image,2,3,0.04) # image, blockSize, kernel size, k
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    return dst

def classify_corners(image):
    x, y = np.nonzero(image) # TODO: Use row, col instead of x, y
    combined = np.array([x,y])
    combined_reshaped = np.reshape(combined, (len(x),-1))
    return combined_reshaped

    kmeans = KMeans(n_clusters = 4).fit(combined_reshaped)
    print(kmeans.cluster_centers_)
    # cv2.imshow('Image Title Goes Here', image)

def main(image):
    log_file = open("log.txt", "w")

    prepped_image = prep_image(image)
    corners = detect_corners(prepped_image)
    # print(corners)

    # image[corners > 0.01 * corners.max()] = [0,0,255] # Threshold for an optimal value, it may vary depending on the image.

    # data = classify_corners(corners)

    print(corners[362][641])

    for i, row in enumerate(corners):
        for j, pixel in enumerate(row):
            if pixel > 0.01:
                # print(i, j)
                log_file.write(str(i) + ' ' + str(j) + '\n')
    log_file.close()



    # cv2.imshow('Image Title Goes Here', corners)
    cv2.imwrite('image.jpg', corners)


    # print(len(x))
    # print(x)
    # print(len(y))
    # print(y)

    # counter = 0
    # for coord in x:
    #     if coord > 200:
    #         counter = counter + 1
    # print(counter, 3347 - counter)

    # counter = 0
    # for coord in y:
    #     if coord > 500:
    #         counter = counter + 1
    # print(counter, 3347 - counter)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # filename = 'images/image0.jpg'
    # filename = 'chessboard.jpg'
    filename = 'simple.jpg'
    image = cv2.imread(filename)
    main(image)
