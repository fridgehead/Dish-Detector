from annoyances import alarms
import time
import sys
import cv
import numpy as np

def main(debug=False, fromCam=False):
  thresh = 200 
  plugradius = [0,0]
  sinkx = [0,0]
  sinky = [0,0]
  #load the sink defs
  f = open("settings", "r")
  for line in f:
    tok = line.split("=")
    if tok[0] == "radius":
      plugradius = [int(p) for p in tok[1].split(",")]
    elif tok[0] == "x":
      sinkx = [int(p) for p in tok[1].split(",")]
    elif tok[0] == "y":
      sinky = [int(p) for p in tok[1].split(",")]
  print "sink at: " + str(sinkx[0]) + ":" + str(sinky[0])

  #get an image
  im = None
  if fromCam == True:
    capture = cv.CaptureFromCAM(0)
    im = cv.QueryFrame(capture)
  else:
    im = cv.LoadImage(sys.argv[1])
  #create grayscale and edge storage
  gray = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  #convert the image to grayscale
  cv.CvtColor(im, gray, cv.CV_BGR2GRAY)
  #check the brightness of the image, if were too dark then exit and shut off alarms

  #edge detect it, then smooth the edges
  cv.Canny(gray, edges, thresh, thresh / 2, 3)
  cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 3, 3) 
 
  #create storage for hough cirlces
  storage = cv.CreateMat(640, 1, cv.CV_32FC3)
  #find the circles
  cv.HoughCircles(gray, storage, cv.CV_HOUGH_GRADIENT, 2, gray.width / 18, thresh, 200,0,0)
 
  #how much shit have we detected?
  detectedShit = 0
  for i in range(storage.rows ):
    val = storage[i, 0] #because numpy arrays are retarded 

    radius = int(val[2])
    center = (int(val[0]), int(val[1]))

    print "circular feature at: " +   str(center), "size: " , str(radius) 
    #try and classify this as sink
    if sinkx[0] - sinkx[1] < center[0] < sinkx[0] + sinkx[1]:
      if sinky[0] - sinky[1] < center[1] < sinky[0] + sinky[1]:
        if plugradius[0] - plugradius[1] < radius < plugradius[0] + plugradius[1]:
	  print "..probably the PLUGHOLE"
          cv.Circle(im, center, radius, (255, 0, 255), 3, 8, 0)
    else:
      print "..probably some unwashed shit"
      detectedShit = detectedShit + 1
      cv.Circle(im, center, radius, (0, 0, 255), 3, 8, 0)



  print "detected shit: ", detectedShit
  alarm = alarms()
  if detectedShit > 0:
    #read the last status from the file. Update it to now
    #also consult the Table-o-Annoyance(tm) to see if we set off an alarm/explosion
    f = open("status","r")
    stat = f.readline().strip()
    f.close()
    if stat == "clean":
       print "last status was : " + stat + ", changing it to DIRTY"
       f = open("status", "w")
       f.write("DIRTY")
       f.close()
       alarm.doAlarm(0) 
    else:
       #just update the shitcounter
       print "updating shit counter"
       f = open("shitcount", "r")
       ct = int(f.readline().strip())
       f.close()
       ct = ct + 1
       if 1 < ct < 2:
	       alarm.doAlarm(0)
       elif 2 < ct < 5:
	       alarm.doAlarm(1)
       f = open("shitcount", "w")
       f.write(str(ct))
       f.close()


  else:
      print "Last status was dirty and now were CLEAN"
      f = open("status", "w")
      f.write("clean")
      f.close()
      print "resetting shitcount"
      f = open("shitcount", "w")
      f.write("0")
      f.close()

      alarm.stopAllAlarms()
  if debug: 
    cv.NamedWindow('Circles')
    cv.ShowImage('Circles', im)
    cv.WaitKey(0)
    cv.ShowImage('Circles', edges)
    cv.WaitKey(0)

if __name__ == '__main__':
  
  main(debug=True, fromCam=True)

