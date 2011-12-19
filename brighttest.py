import sys
import cv

img = cv.LoadImage(sys.argv[1])
hue = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
sat = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
val = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)

cv.CvtColor(img,img, cv.CV_BGR2HSV)
cv.Split(img, hue, sat,val,None)
	
print cv.Avg(val)
exit(0)
cv.NamedWindow('lols')
cv.ShowImage('lols', hue)
cv.WaitKey(0)
cv.ShowImage('lols', sat)
cv.WaitKey(0)

cv.ShowImage('lols', val)
cv.WaitKey(0)
