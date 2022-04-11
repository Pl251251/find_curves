import cv2
import numpy as np

from math import *


# change name of image file
img = cv2.imread("image1.jpg", 1)

height = img.shape[0]
width = img.shape[1]

#pts1 = np.float32([[773, 1968], [2088, 1958], [271, 3257], [2828, 3207]])
pts3 = np.float32([[833, 2140], [2108, 2148], [301, 3367], [2728, 3367]])
pts4 = np.float32([[100, 100], [300, 100], [100, 300], [300, 300]])

matrix = cv2.getPerspectiveTransform(pts3, pts4)
# warp image
image2 = cv2.warpPerspective(img, matrix, (600, 600))
width2 = image2.shape[0]
height2 = image2.shape[1]
cv2.imwrite('test1.jpg', image2)

sum =0
while(1==1):

    #gray and edge
    result = image2[290:300, 91:250]
    cv2.imwrite('test2.jpg', result)
    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    #find lines
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 0, None, 6, 10)
    #sort lines
    c=9000
    d=0

    try:
        for i in linesP:
            l = i[0]
            #cv2.line(result, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
            if (l[0]<c):
                line1 =i
                c= l[0]
            if (l[0]>d):
                line2 =i
                d=l[0]
    except:
        break
    #draw left most and right most lines

    info1 = line1[0]
    info2 =line2[0]
    #cv2.line(result, (info1[0], info1[1]), (info1[2], info1[3]), (0, 0, 255), 3, cv2.LINE_AA)
    #cv2.line(result, (info2[0], info2[1]), (info2[2], info2[3]), (0, 0, 255), 3, cv2.LINE_AA)
    if(abs(info1[1] - info2[1]) <=2):
        y1= int((info1[1] +info2[1])/2)
        y2 =int((info1[3] +info2[3])/2)
        x1 =int(((info1[0]) +int(info2[0]))/2)
        x2 =int((info1[2] +info2[2])/2)
    else:
        y1= int((info1[1] +info2[3])/2)
        y2 =int((info1[3] +info2[1])/2)
        x1 =int(((info1[0]) +int(info2[0]))/2)
        x2 =int((info1[2] +info2[2])/2)
    pt1 = (x1, y1 )
    pt2 = (x2, y2)
    if (y1>y2):
        cv2.arrowedLine(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    elif(y1<y2):
        n = pt2
        pt2 = pt1
        pt1 = n
        cv2.arrowedLine(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    # tranform image back
    cv2.imshow("hope.jpg", image2)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    #rotate image
    try:
        slope = (y2-y1)/(x2-x1)
        rotate = degrees(atan(slope))
        sum1 =sum
        if rotate<0:
            rotate = 90 +rotate
        elif rotate>=0:
            rotate = 90-rotate
        print(rotate)
        sum=rotate+sum

    except:
        rotate =10
        sum1 = sum
        sum= rotate+sum


    #rotate = 360-(90-rotate)
    # rotate our image by 45 degrees around the center of the image
    if sum>90:
        rotate = 90-sum1
        M = cv2.getRotationMatrix2D((300, 300), rotate, 1.0)
        image2= cv2.warpAffine(image2, M, (600, 600))
        break
    else:
        M = cv2.getRotationMatrix2D((300, 300), rotate, 1.0)
        image2= cv2.warpAffine(image2, M, (600, 600))
    cv2.imshow("Rotated_by_x_Degrees.jpg", image2)
    cv2.imwrite("Rotated_by_x_Degrees.jpg", image2)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

pts4 = np.float32([[100, 500], [100, 300], [300, 500], [300, 300]])
matrix2 = cv2.getPerspectiveTransform(pts4, pts3)
final = cv2.warpPerspective(image2, matrix2, (width, height))


roi = img[0:height, 0:width]
# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(final,final,mask = mask)
# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
img[0:height, 0:width ] = dst

cv2.imwrite('final.jpg',img)
