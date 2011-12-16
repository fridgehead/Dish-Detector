import sys
import cv
import numpy as np

def main(thresh):
  im = cv.LoadImage(sys.argv[2])
  bg = cv.LoadImage("test3.jpg")
  graybg = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  gray = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)
  edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)


  cv.CvtColor(bg, graybg, cv.CV_BGR2GRAY)

  cv.CvtColor(im, gray, cv.CV_BGR2GRAY)
  cv.Sub(gray, graybg, gray)
  cv.EqualizeHist(gray,gray)
  cv.Canny(gray, edges, thresh, thresh / 2, 3)
  cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 3, 3) 

  storage = cv.CreateMat(640, 1, cv.CV_32FC3)
  cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 3, gray.width / 18, thresh, 200,0,0)

  for i in range(storage.rows ):
    val = storage[i, 0] 

    radius = int(val[2])
    center = (int(val[0]), int(val[1]))

    print (radius, center)

    cv.Circle(im, center, radius, (0, 0, 255), 3, 8, 0)
    cv.Circle(edges, center, radius, (255, 255, 255), 3, 8, 0)



  print "rows: ", storage.rows
  cv.NamedWindow('Circles')
  cv.ShowImage('Circles', im)
  cv.WaitKey(0)
  cv.ShowImage('Circles', edges)
  cv.WaitKey(0)

if __name__ == '__main__':
  main(int(sys.argv[1]))
