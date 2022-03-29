import cv2
import numpy as np

#change name of image file
img = cv2.imread("image1.jpg",1)

height = img.shape[0]
width = img.shape[1]


pts1 = np.float32([[773, 1968], [2088, 1958],[271, 3257], [2828, 3207]])
pts2 = np.float32([[0, 0], [400, 0], [0, 550], [400, 550]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
#warp image
result = cv2.warpPerspective(img, matrix, (400,550))
width2 =result.shape[0]
height2=result.shape[1]
x1= -100
y1=520
x2=500
y2=520
x3=-100
y3=550
x4=500
y4=550
for x in range(20):
        pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        pts2 = np.float32([[0, 0], [400, 0], [0, 550], [400, 550]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #warp image
        maybe = cv2.warpPerspective(result, matrix, (550,400))
        
        #gray and edge
        gray = cv2.cvtColor(maybe,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)

        #find lines
        linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, 50, 10)
        #sort lines
        c=9000
        d=0
        for i in linesP:
            l = i[0]
            cv2.line(result, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
            if (l[0]<c):
                line1 =i
                c= l[0]
            if (l[0]>d):
                line2 =i
                d=l[0]

        #draw left most and right most lines
        info1 = line1[0]
        info2 =line2[0]
        y1= int((info1[1] +info2[1])/2)
        y2 =int((info1[3] +info2[3])/2)
        pt1 = (int(((info1[0]) +int(info2[0]))/2), y1 )
        pt2 = (int((info1[2] +info2[2])/2), y2)
        if (y1>y2):
            cv2.arrowedLine(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
        elif(y1<y2):
            cv2.arrowedLine(result, pt2, pt1, (255, 0, 0), 1, cv2.LINE_AA)
#tranform image back
matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
final = cv2.warpPerspective(result, matrix2, (width, height))

#use a mask to overlap my images
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


#save image
cv2.imwrite('final.jpg',img)
