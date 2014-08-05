import serial
import sys
import numpy as np
from time import strftime, sleep
import cv2

from common import clock, draw_str
import trig

# Preferences 
prefArduino = 0       #1
prefScreen = 1        #0
prefTargetLead = 1    #1
prefWriteVideo = 0    #1

# create video capture
cap = cv2.VideoCapture(1)

# init video writer
if prefWriteVideo:
  out = cv2.VideoWriter('output/' + strftime("%d%b%Y%H%M%S") + '.avi',cv2.cv.CV_FOURCC(*'MJPG'),20,(640,480))

# serial connection
if prefArduino:
  ser = serial.Serial('/dev/ttyACM0', 115200)

# Definining vars
deltat = 0

while(1):

  _,frame = cap.read()

  if prefWriteVideo:
    out.write(frame) #write to file

  frame = cv2.blur(frame,(3,3)) # smooth it

  hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  # find range of colors

  thresh = cv2.inRange(hsv,np.array((10, 70, 150)), np.array((40, 255, 255)))

  contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) 

  # finding contour with maximum area and store it as best_cnt
  max_area = 0 
  for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > max_area:
          max_area = area
          best_cnt = cnt
  
  if 'best_cnt' in locals():

    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy),5,255,-1)

    #x,y,w,h = cv2.boundingRect(best_cnt)   
    if ('t' in locals()) and prefTargetLead:
      dt = clock() - t  
      print dt 
      a = trig.camToGun(cx,cy, lastCx,lastCy, dt)
    else:
      a = trig.camToGun(cx,cy)

    t = clock()
    lastCx, lastCy = cx, cy
    pan, tilt = a[0], a[1] 

    if prefArduino:
      ser.write("p" + str(pan) + "\n")
      ser.write("t" + str(tilt) + "\n")

  if prefScreen:
    cv2.drawContours(frame,contours,-1,(0,255,0),3) # outline contours 
    if 'dt' in locals():
      draw_str(frame, (20,20), 'time: %.1f ms' % (dt*1000))
    draw_str(frame, (20,50), 'area: %.1f px' % max_area)
    if 'pan' in locals():
      draw_str(frame, (20,80), 'pan: %.1f' % pan)
      draw_str(frame, (20,110), 'tilt: %.1f' % tilt)
    cv2.imshow('frame',frame)
  
  if cv2.waitKey(33)== 27: #Esc keyj
      break

# Clean up everything before leaving
 
cv2.destroyAllWindows()
cap.release()
if prefWriteVideo:
  out.release()
if prefArduino:
  ser.close()
