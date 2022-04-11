import cv2
import numpy as np

from math import *


# change name of image file
img = cv2.imread("image1.jpg", 1)

height = img.shape[0]
width = img.shape[1]

#pts1 = np.float32([[773, 1968], [2088, 1958], [271, 3257], [2828, 3207]])
pts3 = np.float32([[833, 2140], [2108, 2148], [301, 3367], [2728, 3367]])
pts4 = np.float32([[100, 175], [300, 175], [100, 450], [300, 450]])

matrix = cv2.getPerspectiveTransform(pts3, pts4)
# warp image
image2 = cv2.warpPerspective(img, matrix, (600, 900))
width2 = image2.shape[0]
height2 = image2.shape[1]
cv2.imwrite('test1.jpg', image2)


for x in range(20):
    #gray and edge
    result = image2[410:445, 105:250]
    cv2.imwrite('test2.jpg', result)
    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    #find lines
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 0, None, 0, 10)
    #sort lines
    c=9000
    d=0
    for i in linesP:
        l = i[0]
        #cv2.line(result, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
        if (l[0]<c):
            line1 =i
            c= l[0]
        if (l[0]>d):
            line2 =i
            d=l[0]

    #draw left most and right most lines

    info1 = line1[0]
    info2 =line2[0]
    #cv2.line(result, (info1[0], info1[1]), (info1[2], info1[3]), (0, 0, 255), 3, cv2.LINE_AA)
    #cv2.line(result, (info2[0], info2[1]), (info2[2], info2[3]), (0, 0, 255), 3, cv2.LINE_AA)
    y1= int((info1[1] +info2[1])/2)
    y2 =int((info1[3] +info2[3])/2)
    x1 =int(((info1[0]) +int(info2[0]))/2)
    x2 =int((info1[2] +info2[2])/2)
    pt1 = (x1, y1 )
    pt2 = (x2, y2)
    if (y1>y2):
        cv2.arrowedLine(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    elif(y1<y2):
        cv2.arrowedLine(result, pt2, pt1, (255, 0, 0), 1, cv2.LINE_AA)
    # tranform image back
    cv2.imshow("hope.jpg", image2)
    cv2.waitKey(3)
    cv2.destroyAllWindows()
    #rotate image
    try:
        slope = (y2-y1)/(x2-x1)
        rotate = degrees(atan(slope))
        if rotate<0:
            rotate = 90 +rotate
        elif rotate>=0:
            rotate = 90-rotate
        print(rotate)
    except:
        rotate =10
    #rotate = 360-(90-rotate)
    # rotate our image by 45 degrees around the center of the image
    M = cv2.getRotationMatrix2D((300, 450), rotate, 1.0)
    image2= cv2.warpAffine(image2, M, (600, 900))
    cv2.imshow("Rotated_by_x_Degrees.jpg", image2)
    cv2.imwrite("Rotated_by_x_Degrees.jpg", image2)
    cv2.waitKey(3)
    cv2.destroyAllWindows()
