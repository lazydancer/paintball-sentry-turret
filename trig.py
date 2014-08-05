'''
This module contains functions that find the target in space
Assume: 640,480
Units: rads, m
'''
from math import *

def pxToAngle(x,y): # Num -> Num -> (Float, Float)
  '''
  Transforms points on screen to angles in camera

  (320,240) => (0,0); (0,0) => (-24,18); (640,480) => (24,-18)

  The FOV is 60deg with an aspect ratio of 4:3
  x has 48deg, y has 36deg
  Assume: Distance is linear to angle (might be off on the sides)
  ''' 
  return (radians(0.075*x - 24), radians(-0.075*y + 18))

def camPolarCartZ(theta,phi): # Float -> Float -> (Int, Int, Int)
  '''
  Finds the cartesian location from 2 angles and estimating a range
  '''
  z = 5 
  x = z*tan(theta)
  y = z*tan(phi)
    
  return (x,y,z) 

def camPolarCartH(theta,phi,h): # Float -> Float -> Int -> (Int, Int, Int)
  '''
  Find the cartesian location from 2 angles and knowing the height
  of the object
  '''
  objectHeight = 0.54 #wide height 

  z = objectHeight / tan(radians(0.075*h))
  x = z*tan(theta)
  y = z*tan(phi)

  return (x,y,z)


def shiftCart(x,y,z):
  '''
  a,b,c is gun to cam, on relative gun cart
  '''
  a = -0.11
  b = -0.26
  c = 0.15

  return (x+a, y+b, z+c) 

def gunCartToPolar(x,y,z):# Int -> Int -> Int -> (Int, Int)
  '''
  takes a point in space and aims the barrel towards that point
  assumes that the center of rotation of the gun is at the origin

  theta: controls the pan 
  phi:   controls the tilt
  '''
  theta = atan2(x,z)
  phi = atan2(y,z)

  return (theta,phi)

def signalFromPolar(theta,phi):# Rad -> Int
  '''
  Converts the polar angles to actual degrees the servo will use

  Degree = Position Raw Data X 0.325
  (21, 1002) max but probably never should reach that
  512 - Center of rotation
  '''

  a = -degrees(theta) / 0.325 + 538
  b = -degrees(phi) / 0.325 + 488 

  if a < 251 or a > 805:
    print "!!!!!!!!!!! a = " + str(a) + " went beyond 90Deg !!!!!!!!!!!!!"
    return (538,488)
  if b < 211 or b > 765:
    print "!!!!!!!!!!! b = " + str(b) + " went beyond 90Deg !!!!!!!!!!!!!"
    return (538,488)

  return (int(round(a)),int(round(b)))


def computeVelocity(gunCart,lastGunCart,dt):
  '''
  Find the velcocity of the marker
  '''
  v = [0,0,0]
  v[0] = round(((gunCart[0] - lastGunCart[0]) / float(dt)),3)
  v[1] = round(((gunCart[1] - lastGunCart[1]) / float(dt)),3)
  v[2] = round(((gunCart[2] - lastGunCart[2]) / float(dt)),3)

  return v

def estNextPos(gunCart,v,dt):
  '''
  Estimates the position of the marker with velocity
  Uses last clock time to estimate next
  '''
  pos = [0,0,0]
  dt = 0.1
  pos[0] = gunCart[0] + v[0]*dt
  pos[1] = gunCart[1] + v[1]*dt
  pos[2] = gunCart[2] + v[2]*dt

  return pos

def camToGun(cx,cy,lastCx=None,lastCy=None,dt=None):
  '''
  takes the position from the camera
  returns pan and tilt for the turret
  '''


  camAngles = pxToAngle(cx,cy)

  camCart = camPolarCartZ(camAngles[0],camAngles[1])
  #camCart = camPolarCartH(camAngles[0],camAngles[1],h)

  gunCart = shiftCart(camCart[0],camCart[1],camCart[2])
  
  if lastCx is not None:
    lastCamAngles = pxToAngle(lastCx,lastCy)
    lastCamCart = camPolarCartZ(lastCamAngles[0],lastCamAngles[1]) 
    lastGunCart = shiftCart(lastCamCart[0],lastCamCart[1],lastCamCart[2]) 
    v = computeVelocity(gunCart,lastGunCart,dt)
    pos = estNextPos(gunCart,v,dt)
    gunPolar = gunCartToPolar(pos[0],pos[1],pos[2])
  else:
    gunPolar = gunCartToPolar(gunCart[0],gunCart[1],gunCart[2])

  before = gunCartToPolar(gunCart[0],gunCart[1],gunCart[2])
  
  a = signalFromPolar(gunPolar[0],gunPolar[1])
  pan, tilt = a[0], a[1] 
  '''

    if lastGunCart != []:
      v = trig.computeVelocity(gunCart,lastGunCart,dt)
      pos = trig.estNextPos(gunCart,v,dt)
      #print v,pos
    lastGunCart = gunCart
  ''' 
  return a 








