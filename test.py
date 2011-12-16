import sys
import cv


print "Press ESC to exit ..."
capture = cv.CreateCameraCapture(1) 
# create windows
cv.NamedWindow('Camera') 

while 1:
        # do forever
 
        # capture the current frame
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
 
        # mirror
        cv.Flip(frame, None, 1)
        # display webcam image
        cv.ShowImage('Camera', frame)
 
        # handle events
        k = cv.WaitKey(10)
