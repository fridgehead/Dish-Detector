import sys
import cv

img = cv.LoadImage(sys.argv[1])
hue = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
sat = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
val = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)

cv.CvtColor(img,img, cv.CV_BGR2HSV)
cv.Split(img, hue, sat,val,None)
hist = cv.CreateHist([32], cv.CV_HIST_ARRAY, [[0,255]], 1)

cv.CalcHist([sat], hist, 0, None)
avg = 0
for i in range(32):
	va = cv.QueryHistValue_1D(hist, i)
	avg = avg + va
	
print va/32.0

cv.NamedWindow('lols')
cv.ShowImage('lols', hue)
cv.WaitKey(0)
cv.ShowImage('lols', sat)
cv.WaitKey(0)

cv.ShowImage('lols', val)
cv.WaitKey(0)
