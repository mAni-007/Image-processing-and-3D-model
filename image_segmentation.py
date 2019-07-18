import numpy as np 
import cv2
import matplotlib.pyplot as plt 
# from scipy import ndimage


#Reading the Image
image = cv2.imread('recon_1100.tif')
image = cv2.resize(image, (0,0), None, .25, .25)
cv2.imshow('image', image)


#Converting to BGR to Gray
image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#Thresholding the image
th1 = cv2.inRange(image2, 10, 50) #Gray is coke
cv2.imshow('th1', th1)
th2 = cv2.inRange(image2, 50, 255) #white is a iron
# cv2.imshow('th2', th2)



#dilation of a coke
erode = cv2.erode(th1, np.ones((2,2), np.uint8), iterations = 1)
cv2.imshow('erode', erode)
kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closing', closing)
dilation = cv2.dilate(erode, np.ones((2,2), np.uint8), iterations = 1)
cv2.imshow('dilate1', dilation)
#dilation of a iron
dilation2 = cv2.erode(th2, np.ones((3,3), np.uint8), iterations = 1)
# cv2.imshow('dilate2',dilation2)



#Contour formation around the coke and iron
#For Coke
_, contours, _ = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for contour in contours:
	# print(cv2.contourArea(contour))
	if cv2.contourArea(contour) >= 20:
		cv2.drawContours(image, contour, -1, (0, 255, 0), 1)
#For Iron
_, contours, _ = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for contour in contours:
	if cv2.contourArea(contour) >= 15:
		cv2.drawContours(image, contour, -1, (0, 0, 255), 2)

#Display Image
cv2.imshow('img', image)
cv2.waitKey(0)
cv2.destroyAllWindows()



