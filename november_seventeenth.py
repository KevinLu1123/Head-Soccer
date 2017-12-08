#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:20:04 2017
@author: JamesCevasco
"""

#gravity = 2 pixels per second squared for James's computer
#640 is the middle of the screen on James' computer
#radius of a person's head is the average of the width and the height divided by 2
#aka the radius is [(c+d)/2] / 2 = (c+d)/4
#the radius of the ball is 25, this should be unhardcoded eventually

import pdb
import numpy as np
import cv2
import math

badsoccerimg = cv2.imread('SoccerBall.jpg')

soccerimg = cv2.resize(badsoccerimg,None,fx=0.1,fy=0.1,interpolation = cv2.INTER_CUBIC)

safetybouncecount = 0
ballradius = 52
radius = 0 #define them now so they can be used first run through class definitions
ca = 0   
cb = 0
z1 = 0
z2 = 0
xvelocity = 0
yvelocity = 0
head_center = (640,0)
prev_x = head_center[0]
prev_y = head_center[1]
x = 640
y = 0
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
    print ("Ball.position" ,position)
    def boundary (ygravity, height, y, yvelocity):       #450 is for Kevin's screen
        if(y >= 670):
            ygravity = 0
            yvelocity = int(yvelocity * -0.95)
        else:
            ygravity = 2 # constant gravity   
        return ygravity,yvelocity

def velocityx(x, head_center, xvelocity):
    global prev_x
    headvelocity_x = head_center[0] - prev_x
    #print("Head velocity x: ", headvelocity_x)
    #print("prev_x: ", prev_x)
    prev_x = head_center[0]
    #print("2nd prev_x: ", prev_x)
    xvelocity = int(Player.headmass/Ball.mass) * headvelocity_x
    #print("Ball velocity x: ", xvelocity)
    return (headvelocity_x, prev_x, xvelocity)
def velocityy(y, head_center, yvelocity):
    global prev_y
    headvelocity_y = head_center[1] - prev_y
    #print("prev_y: ", prev_y)
    #print("Head velocity y: ", headvelocity_y)
    prev_y = head_center[1]
    #print("2nd prev_y: ", prev_y)
    yvelocity = int(Player.headmass/Ball.mass) * headvelocity_y
    #print("Ball velocity y: ", yvelocity)
    return (headvelocity_y, prev_y, yvelocity)

def hit(radius,x, y, head_center, d, b):
    hit_criteria = radius + ballradius
    print("Hit Criteria:" , hit_criteria, "\n")
    distanceheadball = math.sqrt((ca-x)**2 + (cb-y)**2)
    print("Actual Distance:" , distanceheadball, "\n")
    print(hit_criteria >= distanceheadball)
    eta = 0.000001
    if(hit_criteria >= distanceheadball):# IF this is a hit, then proceed to implement velocity functions
        global slope, xvelocity, yvelocity
        slope = int((y - cb)/(x - ca + eta))
        print("slope: ", slope)
        _, _, xvelocity = velocityx(x,head_center,xvelocity)#Determining the x and y velocities of the ball
        _, _, yvelocity = velocityy(y,head_center,yvelocity)
        #print("xvelocity: ", xvelocity)
        #print("yvelocity: ", yvelocity)
    return (radius,slope,x,y,xvelocity,yvelocity)
    
def xUpdate(radius,x,z1,z2,y):
    radius,_, x, _, xvelocity, _ = hit(radius,x,y,head_center, d, b)#call function for if head hits ball
    x = x + xvelocity #reposition ball based on the hit
    z1,z2,x,y = checkGoal(x,z1,z2,y)
    return(radius,z1,z2,x,y)
    
def yUpdate(safetybouncecount,radius,y,flag):
    #global yvelocity
    radius,_, _, y, _, yvelocity = hit(radius,x,y,head_center, d, b)
    
    ygravity = 2
    
    ygravity,yvelocity = Ball.boundary(ygravity,height, y, yvelocity) # flip direction in the event of a bounce
    
    if(ygravity == 0):
        safetybouncecount = safetybouncecount + 1
    elif(ygravity == 2):
        safetybouncecount = 0
    else:
        print("Something might be wrong:\n\tygravity= ",ygravity,"\n\tsafteybc= ",safetybouncecount)
    
    if(safetybouncecount == 20):
        yvelocity = -50    
    
    yvelocity = yvelocity + ygravity
    
    print("yvelocity + ygravity = " , yvelocity)

    y = y + yvelocity + ygravity #reposition ball based on hit
    
    #print (y)
    return(safetybouncecount, yvelocity, radius,y)

def checkGoal(x,z1,z2,y):
    if x <= 40:
        z2 = scoring(z2,flag)
        x = 640
        y = 0
    if x >= 1200:                 #James's screensize is 1280, has to be resized
        z1 = scoring(z1,flag)
        x = 640
        y = 0
    print("Player 1: ",z1)
    print("Player 2: ",z2)
    return (z1,z2,x,y)
def scoring(z,flag):
    z = z+1
    print(z)
    return z
    
face_cascade = cv2.CascadeClassifier('/Users/JamesCevasco/Desktop/haarcascade_frontalface_default.xml')

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
            ca = int(((2*a)+c)/2)    #(a + half the c/width)
            cb = int(((2*b)+d)/2)    #(b + half the d/height)
            radius = abs(int((c+d)/4))
            diameter = (2*radius)
            cv2.circle(frame, (ca,cb), (radius), (255,0,0), 2)
            
            #print("ca:" , ca , "\n")
            #print("cb:" , cb , "\n")
            #print("radius:" , radius , "\n")
            #print("x:" , x , "\n")
            #print("y:" , y , "\n")
            
            roi_gray = gray[b:b+d, a:a+c]
            roi_color = frame[b:b+d, a:a+c]
            head_center = (ca, cb)

        radius,z1,z2,x,y = xUpdate(radius,x,z1,z2,y)
        
        safetybouncecount,yvelocity,radius,y = yUpdate(safetybouncecount,radius,y,flag)
        
        print("ball position" , ball.position)
      
        #Creation of objects
        
        
        print("The sum isssss: " , (y+(ballradius/2)) - (y-(ballradius/2)) )
        
        cv2.circle(frame,(x,y), ballradius, (150,150,0), -1)
        
        #frame[(x-(ballradius/2)):(x+(ballradius/2)),(y+(ballradius/2)):(y-(ballradius/2))] = soccerimg
            
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
        
        frame = cv2.flip(frame,1)
        
        text1 = str("K: " + str(z1))#str(Player_1.name,": ", str(z1))
        print("text1: ", text1)
        text2 = str("J: " + str(z2))#str(Player_2.name,": ", + str(z2))  
        print("text2: ", text2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.rectangle(frame,(int(0.03125*width),int(0.0694444*height)),(int(0.078125*width),int(0.208333*height)),(255,0,255),-1)
        cv2.putText(frame,text1,(int(0.046875*width),int(0.138888*height)), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.rectangle(frame,(int(0.921875*width),int(0.0694444*height)),(int(0.96875*width),int(0.208333*height)),(0,255,0),-1)
        cv2.putText(frame,text2,(1190,100), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.line(frame,( int(0.03125*width), 0 ),( int(0.03125*width),int(height)),(255,0,255),20)
        cv2.line(frame,( int(0.96875*width), 0 ),( int(0.96875*width),int(height)),(0,255,0),20)
        
        cv2.line(frame,(0,720),(1280,720),(0,255,255),40)
        
        
        cv2.imshow('frame',frame)
        
        
        spacebar = cv2.waitKey(32) & 0xff
        if spacebar == 32:
            z1 = 0
            z2 = 0
            (x,y) = 640,0
            xvelocity = 0
            yvelocity = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
