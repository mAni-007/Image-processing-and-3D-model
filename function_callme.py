import PIL
import Image
import glob
import cv2
import string
import numpy as np 
import xlsxwriter


workbook = xlsxwriter.Workbook('fractions.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Height')
worksheet.write('B1','Coke')
worksheet.write('C1','Void')
worksheet.write('D1','Iron')
worksheet.write('E1','Frac_Coke')
worksheet.write('F1','Frac_Void')
worksheet.write('G1','Frac_Iron')

worksheet.write('E1','Coke')
worksheet.write('F1','Void')
worksheet.write('G1','Iron')


# for i in range(100):
# 	print 'recon_'+ string.zfill(i,4)
i = 0
file = glob.glob('*.tif')
# print file
y = sorted(file)

# take = cv2.imread(y[2400])
# take = cv2.resize(take, (0,0), None, .25, .25)
# cv2.imshow('display', take)
# cv2.waitKey(100)
iterate = 1
counter_length = 0.03
for y[i] in sorted(file):
	print y[i]
	# WARNING ......... DON'T MIX THE 'IMAGE' AND 'PICTURES'. THESE ARE TWO DIFFERENT ENTITIES.
	# TWO DIFFERENT APPROACH

	#Reading Image for Coke
	image = cv2.imread(y[i])
	image = cv2.resize(image, (0,0), None, .25, .25)
	cv2.imshow('image', image)
	print image.shape

	#Reading Picture for Iron
	pic = cv2.imread(y[i])
	pic = cv2.resize(pic, (0,0), None, .25, .25)



	# Extracting the Inner Radius of Crucible
	# Black background with white filled circle 
	# Masked over the the Image of coke 
	black_background = np.zeros((image.shape[0],image.shape[1],image.shape[2]), dtype = 'uint8')
	cv2.circle(black_background, (314, 320), 248, (255,255,255), -1)

	whiteBlack1channel = cv2.cvtColor(black_background, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(whiteBlack1channel, 220, 255, cv2.THRESH_BINARY)

	# Contour formation of Circle to extract only inner part of the crucible
	_, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	Crucible_area = 0
	for contour in contours:
		cv2.drawContours(image, contours, -1, (240, 200, 100), 1)
		Crucible_area = cv2.contourArea(contour)
	print "Crucible_area = ",Crucible_area
	# cv2.imshow('bla', mask)

	# Masked over the original image 
	img2_fg = cv2.bitwise_and(image,image,mask = mask)
	image2 = cv2.cvtColor(img2_fg, cv2.COLOR_BGR2GRAY)



	# COKE AREA CALCULATION ............


	# Manipulation only for coke area
	# THresholding with morphologyEx which reduce the black pixel inside the white area
	# Drawing External Contour so that it do not double count the inside contour

	th1 = cv2.inRange(image2, 15, 25)
	kernel = np.ones((4,4), np.uint8)
	closing_coke = cv2.morphologyEx(th1, cv2.MORPH_CLOSE, kernel)
	kernel = np.ones((2,2), np.uint8)
	opening_coke = cv2.morphologyEx(closing_coke, cv2.MORPH_OPEN, kernel)

	_, contours, _ = cv2.findContours(opening_coke, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	coke_area = 0
	for contour in contours:
		if cv2.contourArea(contour) > 50:
			cv2.drawContours(image, contour, -1, (0, 255, 0), 1)
			coke_area = cv2.contourArea(contour) + coke_area
			
	print 'coke_area =', coke_area


	#  IRON AREA CALCULATION ............

	#  Maipulation only in iron area
	#  Used the original Image as it was
	#  Avoid using circular method as was used in Coke Calculation

	pic2 = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
	th2 = cv2.inRange(pic2, 70, 255)
	kernel = np.ones((3,3), np.uint8)
	closing_iron = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)

	# Contour formation which will be External no Tree contour
	Iron_area = 0
	_, contours, _ = cv2.findContours(closing_iron, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	for contour in contours:
		cv2.drawContours(image, contour, -1, (0, 0, 255), -1)
		Iron_area = cv2.contourArea(contour) + Iron_area
	print 'Iron_area =', Iron_area



	# Showcase all the Outcome
	# cv2.imshow('img_iron', pic)
	cv2.imshow('img_coke', image)
	cv2.imshow('close_iron', closing_iron)
	cv2.imshow('open_coke', opening_coke)
	cv2.imshow('th2_iron', th2)
	cv2.imshow('close_coke', closing_coke)
	cv2.imshow('th1_coke', th1)



	# Displaying the Fraction of Everything	
	# Include Coke, Iron and Void
	void = Crucible_area - Iron_area - coke_area
	print 'void = ', void

	Fraction_of_Coke = coke_area/Crucible_area*100
	Fraction_of_Iron = Iron_area/Crucible_area*100
	Fraction_of_Void = void/Crucible_area*100

	print 'Fraction of coke = ',Fraction_of_Coke,'%'
	print 'Fraction of Iron = ',Fraction_of_Iron,'%'
	print 'Fraction of Void = ',Fraction_of_Void,'%'


	# Time to save Data to excel sheet

	worksheet.write( iterate, 0, counter_length)
	worksheet.write( iterate, 1, coke_area)
	worksheet.write( iterate, 2, void)
	worksheet.write( iterate, 3, Iron_area)
	worksheet.write( iterate, 4, Fraction_of_Coke)
	worksheet.write( iterate, 5, Fraction_of_Void)
	worksheet.write( iterate, 6, Fraction_of_Iron)
	worksheet.write(iterate, 7, Fraction_of_Iron)
	worksheet.write(iterate, 8, Fraction_of_Iron)
	worksheet.write(iterate, 8, Fraction_of_Iron)



	# Increment by 1 and 0.03 for height
	iterate = iterate + 1
	counter_length = counter_length + 0.03
	i = i + 1
	
	# Wait for 10ms
	cv2.waitKey(1000000)

workbook.close()
cv2.destroyAllWindows()