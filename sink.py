from annoyances import alarms
import time
import sys
import cv

#calculate the average brightness of an image
#used to work out if its night time and turn the alarms off
def getBrightness(img):
  hue = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
  sat = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
  val = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
  test = cv.CloneImage(img)
  cv.CvtColor(img,test, cv.CV_BGR2HSV)
  cv.Split(img, hue, sat,val,None)
  	
  return cv.Avg(val)[0]

'''
debug = displays a cv window with each stage in it. Doesnt work on headless servers
fromCam = use the camera as the image source, if False then load an image supplied by sys.argv[1]
'''
def main(debug=False, fromCam=False):
  # threshold for canny edge detect
  thresh = 200 
  #min and max radius for the plughole
  plugradius = [0,0]
  #coordinates of the plughole [coord, +-tolerance]
  sinkx = [0,0]
  sinky = [0,0]
  #load the sink defs from settings
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

  # get an image from our source
  im = None
  if fromCam == True:
    capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
    im = cv.QueryFrame(capture)
  else:
    im = cv.LoadImage(sys.argv[1])
  #work out the brightness of the image
  bright = getBrightness(im)
  print "image brightness = " , bright
  #lets see if its too dark and we should shut the alarms up
  if bright < 30:
	  alarm = alarms()
	  alarm.stopAllAlarms()
	  print "Stopping all alarms as its night time, alarms count will continue in the morning"
	  exit()

  #create grayscale and edge storage
  gray = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  #convert the image to grayscale
  cv.CvtColor(im, gray, cv.CV_BGR2GRAY)

  #edge detect it, then smooth the edges
  cv.Canny(gray, edges, thresh, thresh / 2, 3)
  cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 3, 3) 
 
  #create storage for hough cirlces
  storage = cv.CreateMat(640, 1, cv.CV_32FC3)
  #find the circles, most of these parameters are magic numbers that work well enough for where the camera is installed
  cv.HoughCircles(gray, storage, cv.CV_HOUGH_GRADIENT, 2, gray.width / 18, thresh, 300,0,0)
 
  #how much crap have we detected?
  detectedShit = 0
  #for each circle detected...
  for i in range(storage.rows ):
    val = storage[i, 0] #because numpy arrays are retarded 

    radius = int(val[2])
    center = (int(val[0]), int(val[1]))

    print "circular feature at: " +   str(center), "size: " , str(radius) 
    sinkFound = False
    #try and classify this as sink
    if sinkx[0] - sinkx[1] < center[0] < sinkx[0] + sinkx[1]:
      if sinky[0] - sinky[1] < center[1] < sinky[0] + sinky[1]:
	#plugradius is now min/max
        if plugradius[0]  < radius < plugradius[1]:
	  print "..probably the PLUGHOLE"
          cv.Circle(im, center, radius, (255, 0, 255), 3, 8, 0)
	  sinkFound = True
	else:
	  print "..PH failed radius check"
      else:
          print "..PH failed Y check"
    
    else:
      print "..PH failed X check"
    if not sinkFound:
      print "..probably some unwashed crap"
      detectedShit = detectedShit + 1
      cv.Circle(im, center, radius, (0, 0, 255), 3, 8, 0)


  print "detected crap: ", detectedShit
  #create our alarm object to trigger annoyances
  alarm = alarms()
  if detectedShit > 0:
    #read the last status from the file. Update it to now
    #also consult the Table-o-Annoyance(tm) to see if we set off an alarm/explosion
    #lots of this could be tidied up but I DONT CARE
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
       #just update the crapcounter
       print "updating crap counter"
       f = open("crapcount", "r")
       ct = int(f.readline().strip())
       f.close()
       ct = ct + 1
       if 1 < ct < 2:
	       alarm.doAlarm(0)
       elif 2 < ct < 5:
	       alarm.doAlarm(1)
       elif ct >= 5:
               alarm.doAlarm(2)
       f = open("crapcount", "w")
       f.write(str(ct))
       f.close()


  else:
      print "Last status was dirty and now we're CLEAN"
      f = open("status", "w")
      f.write("clean")
      f.close()
      print "resetting crapcount"
      f = open("crapcount", "w")
      f.write("0")
      f.close()
      # kill ALL the alarms \o/
      alarm.stopAllAlarms()
  #if debugging then display each stage of the process in a cv windows. Useful when configuring things
  if debug: 
    cv.NamedWindow('Circles')
    cv.ShowImage('Circles', im)
    cv.WaitKey(0)
    cv.ShowImage('Circles', edges)
    cv.WaitKey(0)

if __name__ == '__main__':
  #print change these options when fiddling
  main(debug=False, fromCam=True)
