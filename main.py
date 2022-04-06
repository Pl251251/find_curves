import cv2
import numpy as np

# change name of image file
img = cv2.imread("image2.jpg", 1)

height = img.shape[0]
width = img.shape[1]

#pts1 = np.float32([[773, 1968], [2088, 1958], [271, 3257], [2828, 3207]])
pts3 = np.float32([[853, 2208], [2108, 2208], [351, 3307], [2628, 3307]])
pts4 = np.float32([[0, 0], [400, 0], [0, 550], [400, 550]])

matrix = cv2.getPerspectiveTransform(pts3, pts4)
# warp image
result = cv2.warpPerspective(img, matrix, (400, 550))
width2 = result.shape[0]
height2 = result.shape[1]
cv2.imwrite('test1.jpg', result)
x1 = 0
y1 = 500
x2 = 400
y2 = 500
x3 = 0
y3 = 550
x4 = 400
y4 = 550
for x in range(1):
    pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    pts2 = np.float32([[0, 0], [400, 0], [0, 50], [400, 50]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # warp image
    maybe = cv2.warpPerspective(result, matrix, (400, 50))
    cv2.imwrite('maybe.jpg', maybe)

    matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
    test1 = cv2.warpPerspective(maybe, matrix2, (400, 550))
    cv2.imwrite("test6.jpg", test1)

    # gray and edge

    """
        gray = cv2.cvtColor(maybe, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # find lines
        linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, 30, 10)
        # sort lines
        c = 9000
        d = 0
        try:
            for i in linesP:
                l = i[0]
                cv2.line(maybe, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv2.LINE_AA)
                if (l[0] < c):
                    line1 = i
                    c = l[0]
                if (l[0] > d):
                    line2 = i
                    d = l[0]
        except:
            line1 =[[10,20,30,40]]
            line2 =[[10,30,20,40]]

        cv2.line(maybe, (line1[0][0], line1[0][1]), (line1[0][2], line1[0][3]), (255, 0, 255), 3, cv2.LINE_AA)
        cv2.line(maybe, (line2[0][0], line2[0][1]), (line2[0][2], line2[0][3]), (255, 0, 255), 3, cv2.LINE_AA)
        cv2.imwrite('line.jpg', maybe)
        # draw left most and right most lines
        info1 = line1[0]
        info2 = line2[0]
        y1 = int((info1[1] + info2[3]) / 2)
        y2 = int((info1[3] + info2[1]) / 2)
        pt1 = (int((info1[0] + info2[0]) / 2), y1)
        pt2 = (int((info1[2] + info2[2]) / 2), y2)
        if (y1 > y2):
            cv2.arrowedLine(maybe, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
        elif (y1 < y2):
            n= pt2
            pt2=pt1
            pt1=n
            cv2.arrowedLine(maybe, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imwrite('arrow.jpg', maybe )
        (info1, info2) =pt1
        (info3,info4) =pt2
        (info5,info6) = ((info3-info1),info4-info2)
        x1 = info3- 5*info6 + info5
        y1 = info4 - 5*info5 +info6
        x2 = info3+5*info6 + info5
        y2 = info4 + 5*info5 +info6
        x3 = info3- 5*info6
        y3 = info4 - 5*info5
        x4 = info3+ 5*info6
        y4 = info4 + 5*info5
        cv2.imwrite("test4.jpg", maybe)
        matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
        test1 = cv2.warpPerspective(maybe, matrix2, (400, 550))
        cv2.imwrite("test6.jpg", test1)
        roi = result[0:550, 0:400]
        # Now create a mask of logo and create its inverse mask also
        img2gray = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(test1, test1, mask=mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg, img2_fg)
        result[0:550, 0:400] = dst
        cv2.imwrite("result1.jpg",result)
    """
    gray = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # find lines
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, 30, 30)
    # sort lines
    c = 9000
    d = 0
    try:
        for i in linesP:
            l = i[0]
            cv2.line(test1, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv2.LINE_AA)
            if (l[0] < c):
                line1 = i
                c = l[0]
            if (l[0] > d):
                line2 = i
                d = l[0]
    except:
        line1 =[[10,20,30,40]]
        line2 =[[10,30,20,40]]

    cv2.line(test1, (line1[0][0], line1[0][1]), (line1[0][2], line1[0][3]), (255, 0, 255), 3, cv2.LINE_AA)
    cv2.line(test1, (line2[0][0], line2[0][1]), (line2[0][2], line2[0][3]), (255, 0, 255), 3, cv2.LINE_AA)
    cv2.imwrite('line.jpg', test1)
    # draw left most and right most lines
    info1 = line1[0]
    info2 = line2[0]
    y1 = int((info1[1] + info2[3]) / 2)
    y2 = int((info1[3] + info2[1]) / 2)
    pt1 = (int((info1[0] + info2[0]) / 2), y1)
    pt2 = (int((info1[2] + info2[2]) / 2), y2)
    if (y1 > y2):
        cv2.arrowedLine(test1, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    elif (y1 < y2):
        n= pt2
        pt2=pt1
        pt1=n
        cv2.arrowedLine(test1, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.imwrite('arrow.jpg', test1 )
    (info1, info2) =pt1
    (info3,info4) =pt2
    (info5,info6) = ((info3-info1),info4-info2)
    x1 = info3- 5*info6 + info5
    y1 = info4 - 5*info5 +info6
    x2 = info3+5*info6 + info5
    y2 = info4 + 5*info5 +info6
    x3 = info3- 5*info6
    y3 = info4 - 5*info5
    x4 = info3+ 5*info6
    y4 = info4 + 5*info5
    cv2.imwrite("test4.jpg", test1)
    """
    matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
    test1 = cv2.warpPerspective(maybe, matrix2, (400, 550))
    cv2.imwrite("test6.jpg", test1)
    """
    roi = result[0:550, 0:400]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(test1, test1, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    result[0:550, 0:400] = dst
    cv2.imwrite("result1.jpg",result)


# tranform image back
matrix3 = cv2.getPerspectiveTransform(pts4, pts3)
final = cv2.warpPerspective(result, matrix3, (width, height))
cv2.imwrite("final1.jpg",final)
# use a mask to overlap my images
roi = img[0:height, 0:width]
# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(final, final, mask=mask)
# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg, img2_fg)
img[0:height, 0:width] = dst

# save image
cv2.imwrite('final.jpg', img)
