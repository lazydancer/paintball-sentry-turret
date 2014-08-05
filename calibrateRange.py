import cv2
import numpy as np
from common import clock, draw_str



cap = cv2.VideoCapture(1)

def nothing(x):
  pass

cv2.namedWindow('frame')
cv2.createTrackbar('H-','frame',0,255,nothing)
cv2.createTrackbar('H+','frame',0,255,nothing)
cv2.setTrackbarPos('H+','frame',255)
cv2.createTrackbar('S-','frame',0,255,nothing)
cv2.createTrackbar('S+','frame',0,255,nothing)
cv2.setTrackbarPos('S+','frame',255)
cv2.createTrackbar('V-','frame',0,255,nothing)
cv2.createTrackbar('V+','frame',0,255,nothing)
cv2.setTrackbarPos('V+','frame',255)

while(1):

  _,frame = cap.read()
  frame = cv2.blur(frame,(3,3)) # smooth it

  hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)   
  hLow = cv2.getTrackbarPos('H-','frame')
  hHigh = cv2.getTrackbarPos('H+','frame')
  sLow = cv2.getTrackbarPos('S-','frame')
  sHigh = cv2.getTrackbarPos('S+','frame')
  vLow = cv2.getTrackbarPos('V-','frame')
  vHigh = cv2.getTrackbarPos('V+','frame')
  
  thresh = cv2.inRange(hsv,np.array((hLow, sLow, vLow)), np.array((hHigh, sHigh, vHigh)))

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


  cv2.drawContours(frame,contours,-1,(0,255,0),3) # outline contours 
  draw_str(frame, (20,50), 'area: %.1f px' % max_area)
  cv2.imshow('frame',frame)

  if cv2.waitKey(33)== 27: #Esc keyj
      break

# Clean up everything before leaving
 
cv2.destroyAllWindows()
cap.release()
