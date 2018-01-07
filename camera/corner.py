import cv2
import numpy as np

# filename = 'images/image0.jpg'
# filename = 'chessboard.jpg'
filename = 'simple.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04) # image, blockSize, kernel size, k


# result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
cv2.imshow('Image Title Goes Here', dst)

# Create a binary for findNonZero
# retval, thresh = cv2.threshold(dst, thresh=100, maxval=1, type=cv2.THRESH_BINARY)
# print(type(retval))
# print(type(thresh))
# print(sum(sum(dst)))

# test = np.array([0,0,0,0,1])

x, y = np.nonzero(dst)
for i, x in enumerate(x):
    print(x,y)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

# Threshold for an optimal value, it may vary depending on the image.
# img[dst > 0.01 * dst.max()] = [0,0,255]


# https://code.ros.org/trac/opencv/browser/trunk/opencv/modules/core/include/opencv2/core/types_c.h?rev=3837
# CV_8UC1
