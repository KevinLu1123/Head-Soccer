# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:27:10 2017

@author: junlu
"""

#import numpy as np
import cv2
import math

z1 = 0
z2 = 0
xvelocity = 0
yvelocity = 0
head_center = (320,240)
prev_x = head_center[0]
prev_y = head_center[1]
x = 320
y = 240
slope = 0
#def ballmovementcollision(x,ca,y,cb,slope):
#    y = slope * (x - ca) + cb
class Player():
    mass = 140
    #def _init_(self, name = "", mass = 0):
        #self.name = name
        #self.mass = mass * 0.072 # Needs to be changed later on
    headmass = mass * 0.072 # ask for graphical input - lbs

class Ball():
    mass = 8 # currently an arbitrary number, maybe ask for body weight input later. Head = 0.072 x body weight
    #direction = slope
    speed = 0 #speed is determined by speed of head x mass of head / mass of ball
    position = (x,y)
    print (position)
    def boundary (y, yvelocity):
        if y >= 450:
            yvelocity = yvelocity * -1
        return yvelocity

def velocityx(x, head_center, xvelocity):
    global prev_x
    headvelocity_x = head_center[0] - prev_x
    print("Head velocity x: ", headvelocity_x)
    print("prev_x: ", prev_x)
    prev_x = head_center[0]
    print("2nd prev_x: ", prev_x)
    xvelocity = int(Player.headmass/Ball.mass) * headvelocity_x
    print("Ball velocity x: ", xvelocity)
    return (headvelocity_x, prev_x, xvelocity)
def velocityy(y, head_center, yvelocity):
    global prev_y
    headvelocity_y = head_center[1] - prev_y
    print("prev_y: ", prev_y)
    print("Head velocity y: ", headvelocity_y)
    prev_y = head_center[1]
    print("2nd prev_y: ", prev_y)
    yvelocity = int(Player.headmass/Ball.mass) * headvelocity_y
    print("Ball velocity y: ", yvelocity)
    return (headvelocity_y, prev_y, yvelocity)

def hit(x, y, head_center, d, b):
    hit_criteria = (d-b) + 25
    distanceheadball = math.sqrt((head_center[0]-x)**2 + (head_center[1]-y)**2)
    print(hit_criteria >= distanceheadball)
    eta = 0.000001
    if(hit_criteria >= distanceheadball):# IF this is a hit, then proceed to implement velocity functions
        global slope, xvelocity, yvelocity
        slope = int((y - cb)/(x - ca + eta))
        print("slope: ", slope)
        _, _, xvelocity = velocityx(x,head_center,xvelocity)#Determining the x and y velocities of the ball
        _, _, yvelocity = velocityy(y,head_center,yvelocity)
        print("xvelocity: ", xvelocity)
        print("yvelocity: ", yvelocity)
    return (slope,x,y,xvelocity,yvelocity)
    
def xUpdate(x,z1,z2,y):
    _, x, _, xvelocity, _ = hit(x,y,head_center, d, b)#call function for if head hits ball
    if (x <= 40):
        x = 40
    if (x >= 560):
        x = 560
    else:
        x = x + xvelocity #reposition ball based on the hit
    z1,z2,x,y = checkGoal(x,z1,z2,y)
    return(z1,z2,x,y)
def yUpdate(y,flag):
    global yvelocity
    _, _, y, _, yvelocity = hit(x,y,head_center, b, d)
    ygravity = 2 # constant gravity
    yvelocity = Ball.boundary(y, yvelocity) # flip direction in the event of a bounce
    if y >= 450:
        y = 450 + yvelocity
    else:
        y = y + yvelocity + ygravity #reposition ball based on hit
    
    #print (y)
    return(y)

def checkGoal(x,z1,z2,y):
    if x <= 40:
        z2 = scoring(z2,flag)
        x = 320
        y = 240
    if x >= 560:
        z1 = scoring(z1,flag)
        x = 320
        y = 240
    print("Player 1: ",z1)
    print("Player 2: ",z2)
    return (z1,z2,x,y)
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

flag = True
targetScore = 5

Player_1 = Player()#"Kevin",140)#Give stats of players
Player_2 = Player()#"James",140)
ball = Ball()

b = 0
d = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (a,b,c,d) in faces:# abcd are just xywh but xyz already used earlier
            global b, d
            diameter = d            
            ca = int((2*a+c)/2)
            cb = int((2*b+d)/2)
            cv2.circle(frame, (ca,cb), (int(d/1.75)), (255,0,0), 2)#radius must be changed for different computers/different screens
            roi_gray = gray[b:b+d, a:a+c]
            roi_color = frame[b:b+d, a:a+c]
            head_center = (ca, cb)

        z1,z2,x,y = xUpdate(x,z1,z2,y)
        y = yUpdate(y,flag)
        print(ball.position)
        #Creation of objects
        text1 = str("K: " + str(z1))#str(Player_1.name,": ", str(z1))
        print("text1: ", text1)
        text2 = str("J: " + str(z2))#str(Player_2.name,": ", + str(z2))  
        print("text2: ", text2)
        frame = cv2.flip(frame,1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame,(40,50),(100,150),(255,0,255),3)
        cv2.putText(frame,text1,(60,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.rectangle(frame,(540,50),(600,150),(0,255,0),3)
        cv2.putText(frame,text2,(550,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.line(frame,(40,0),(40,500),(255,0,255),20)
        cv2.line(frame,(600,0),(600,600),(0,255,0),20)
        cv2.line(frame,(0,480),(640,480),(0,255,255),40)
        cv2.circle(frame,(x,y), 25, (150,150,0), -1)    
            
        if (z1-z2) >= 2 and z1 >= targetScore:
            flag = False
            cv2.rectangle(frame,(150,100),(500,200),(255,0,255),3)
            cv2.putText(frame, "K Wins!",(150,180), font, 3,(255,0,255),2,cv2.LINE_AA)#str(Player_1.name," Wins!"),(150,180), font, 3,(255,0,255),2,cv2.LINE_AA)
        if (z2-z1) >= 2 and z2 >= targetScore:
            flag = False
            cv2.rectangle(frame,(150,100),(500,200),(0,255,0),3)
            cv2.putText(frame,"J Wins!",(150,180), font, 3,(0,255,0),2,cv2.LINE_AA)#str(Player_2.name," Wins!"),(150,180), font, 3,(0,255,0),2,cv2.LINE_AA)
        print("Summary List: ")
        print("******************************************************************")
        cv2.imshow('frame',frame)
        spacebar = cv2.waitKey(32) & 0xff
        if spacebar == 32:
            z1 = 0
            z2 = 0
            (x,y) = 320,240
            xvelocity = 0
            yvelocity = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()