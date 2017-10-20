# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:27:10 2017

@author: junlu
"""

import numpy as np
import cv2
import math

z1 = 0
z2 = 0

def ballmovementcollision(x,ca,y,cb,t,slope):
    y = slope*(x - ca) + cb

def tUpdate(t,flag):
    if flag:
        t = t + 1
        #print (t)
    return(t)
def xUpdate(t,x,z1,z2,flag,diameter):
    x = 300
    #print (x)
    if x == 40:
        z2 = scoring(z2,flag)
        print(z2)
        x = 200
        t = 0
    if x == 560:
        z1 = scoring(z1,flag)
        print(z1)
        x = 200
        t = 0
        
    ball_center = (ca, cb)
    hit_criteria = (diameter/1.75) + 25
    distanceheadball = math.sqrt((ball_center[0]-x)**2 + (ball_center[1]-y)**2)
    
    eta = 0.000001
    if(hit_criteria >= distanceheadball):
        slope = int((y - cb)/(x - ca + eta))
        
    return(x,z1,z2,t)
def yUpdate(t,y,flag):
    y = 4*t + 200
    if y == 600:
        t = 0
    #print (y)
    return(y)

def scoring(z,flag):
    z = z+1
    print(z)
    return z
    
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if(ret == False):
    cap = cv2.VideoCapture(0)
width = cap.get(3)  # float
height = cap.get(4) # float
print(width, height)
        
# Define the codec and create VideoWriter object

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))#frame size adjust
# img = np.zeros((512,512,3), np.uint8)
t = 0
x = 50
y = 50
flag = True
targetScore = 5

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (a,b,c,d) in faces:# abcd are just xywh but xyz already used earlier
            diameter = d            
            ca = int((2*a+c)/2)
            cb = int((2*b+d)/2)
            cv2.circle(frame, (ca,cb), (int(d/1.75)), (255,0,0), 2)#radius must be changed for different computers/different screens
            roi_gray = gray[b:b+d, a:a+c]
            roi_color = frame[b:b+d, a:a+c]

            
            t = tUpdate(t,flag)
            x,z1,z2,t = xUpdate(t,x,z1,z2,flag,diameter)
            y = yUpdate(t,y,flag)
        
        #Creation of objects
        text1 = "K: " + str(z1)
        text2 = "J: " + str(z2)
        
        frame = cv2.flip(frame,1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame,(40,50),(100,150),(255,0,255),3)
        cv2.putText(frame,text1,(60,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.rectangle(frame,(540,50),(600,150),(0,255,0),3)
        cv2.putText(frame,text2,(550,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.line(frame,(40,0),(40,500),(255,0,255),20)
        cv2.line(frame,(600,0),(600,600),(0,255,0),20)
        
        cv2.circle(frame,(x,y), 25, (255,255,255), -1)    
            
        if (z1-z2) >= 2 and z1 >= targetScore:
            flag = False
            cv2.rectangle(frame,(150,100),(500,200),(255,0,255),3)
            cv2.putText(frame,"K Wins!",(150,180), font, 3,(255,0,255),2,cv2.LINE_AA)
        if (z2-z1) >= 2 and z2 >= targetScore:
            flag = False
            cv2.rectangle(frame,(150,100),(500,200),(0,255,0),3)
            cv2.putText(frame,"J Wins!",(150,180), font, 3,(0,255,0),2,cv2.LINE_AA)
           
        cv2.imshow('frame',frame)
        spacebar = cv2.waitKey(32) & 0xff
        if spacebar == 32:
            z1 = 0
            z2 = 0
            t = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()