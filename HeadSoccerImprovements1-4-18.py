# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10:27:10 2017

@author: Kevin Lu
"""

#import numpy as np
import cv2
import math
import time
import tkinter
import pdb
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)

ret, frame = cap.read()
if(ret == False):
    cap = cv2.VideoCapture(0)
width = int(cap.get(3))  # float
height = int(cap.get(4)) # float 

z1 = 0
z2 = 0

xvelocity, yvelocity = 0,0

headvelocity_x,headvelocity_y = 0,0

x,y = width/2,0

prev_x,prev_y = 0,0
#def ballmovementcollision(x,ca,y,cb,slope):
#    y = slope * (x - ca) + cb
class Ball():
    mass = 8 # currently an arbitrary number, maybe ask for body weight input later. Head = 0.072 x body weight
    #direction = slope
    speed = 0 #speed is determined by speed of head x mass of head / mass of ball
    x_position = width/2
    y_position = 0
    
    def boundary (ygravity, y, yvelocity):
        if(y >= height-30):
            ygravity = 0
            yvelocity = int(yvelocity * -0.9)
        else:
            ygravity = 2 # constant gravity   
        return ygravity,yvelocity
ball = Ball()
    
x,y = ball.x_position,ball.y_position
   
class Player():
    def __init__(self, name = "", mass = 140):
        super().__init__()
        self.name = name
        self.headmass = mass * 0.072 # Needs to be changed later on
        #self.headmass = self.mass * 0.072 # ask for graphical input - lbs
#        if self.head_center == None:         This doesn't work right now, butI suspect this will help with the fact that headvelocity_y is always 0 bc prev_y and headvelocity_y are always the same, which is wrong.
 #           self.prev_x = 0                       Should be the same case for headvelocity_x, which is perhaps why xvelocity does not change or changes once from an initial value, and why yvelocity stays 0.
  #          self.prev_y = 0
        self.head_center = (int(width/2),int(height/2))#affecting the headballdistance calculation
        self.prev_x = self.head_center[0]
        self.prev_y = self.head_center[1]
        #self.head_radius = 25
    def velocityx(self, x, head_center):
        global prev_x
        headvelocity_x = (head_center[0] - prev_x)
        prev_x = head_center[0]
        return (headvelocity_x, prev_x)

    def velocityy(self,y, head_center):
        global prev_y
        headvelocity_y = (head_center[1] - prev_y)
        prev_y = head_center[1]
        print("Head velocity y: ", headvelocity_y)
        return (headvelocity_y, prev_y)
        
    def hit(self,x,y):
        self.hit_criteria = head_radius + 25
        self.distanceheadball = math.sqrt((self.head_center[0]-ball.x_position)**2 + (self.head_center[1]-ball.y_position)**2)
        print("Hit: ",(self.hit_criteria >= self.distanceheadball))
        #print("x: ",x)
        #print("y: ",y)
        print(self.head_center[0]-ball.x_position, "______", self.head_center[1]-ball.y_position)
        print("ball x: ", ball.x_position)
        print("ball y: ", ball.y_position)
        print("headcenter[x]: ",head_center[0])
        print("headcenter[y]: ",head_center[1])
        print("radii sum: ", self.hit_criteria)
        print("distance between head and ball centers: ", self.distanceheadball)
        print("head_radius: ", head_radius)
        return(self.hit_criteria >= self.distanceheadball)# IF this is a hit, then proceed to implement velocity functions
    
    def hitresult(self,b,xvelocity,yvelocity):   
        if(self.hit_criteria >= self.distanceheadball):# IF this is a hit, then proceed to implement velocity functions
            #global slope, xvelocity, yvelocity
            #eta = 0.000001
            #slope = int((ball.y_position - center_y)/(ball.x_position - center_x + eta))
            headvelocity_x, _ = self.velocityx(ball.x_position,head_center)#Determining the x and y velocities of the ball
            headvelocity_y, _ = self.velocityy(ball.y_position,head_center)
        #print("HIT: ", hit_criteria >= distanceheadball)
        #print("radii sum: ", hit_criteria)
        #print("distance between head and ball centers: ", distanceheadball)
        return(ball.x_position,ball.y_position,xvelocity,yvelocity,headvelocity_x,headvelocity_y)

def x_momentumconservation(P,headvelocity_x,xvelocity):
    xvelocity = -1*int(P.headmass/ball.mass) * headvelocity_x
    return xvelocity

def y_momentumconservation(P,headvelocity_y,yvelocity):
    yvelocity = -1*int(P.headmass/ball.mass) * headvelocity_y
    return yvelocity
    
def redefineHeadLocation(P):
    P.head_center = (center_x,center_y)
    return P.head_center
    
Player_1 = Player()#Give stats of players
Player_2 = Player()
      
def xUpdate(P,xvelocity,yvelocity):
    if P != None:
        ball.x_position, _, xvelocity, _, headvelocity_x, _ = P.hitresult(ball,xvelocity,yvelocity)#call function for if head hits ball
        print("Ball velocity x: ", xvelocity)
        print("Ball velocity y: ", yvelocity)
        return (ball.x_position, xvelocity, headvelocity_x)
    return (ball.x_position, xvelocity)
    #Gap due to function being moved out of here, which is causing problems.

def final_x(xvelocity):
    ball.x_position = ball.x_position + xvelocity #reposition ball based on the hit
    x = ball.x_position
    return(ball.x_position,xvelocity,x)

    
safetybouncecount = 0
def yUpdate(safetybouncecount,P,xvelocity,yvelocity,headvelocity_y):
    if P != None:
        _, ball.y_position, _, yvelocity, _, headvelocity_y = P.hitresult(ball,xvelocity,yvelocity)
        print("Ball velocity x: ", xvelocity)
        print("Ball velocity y: ", yvelocity)
        return(ball.y_position, yvelocity, headvelocity_y)
    return (ball.x_position, xvelocity)
def final_y(yvelocity,safetybouncecount):
    ygravity = 2
    ygravity,yvelocity = Ball.boundary(ygravity, ball.y_position, yvelocity)    
    if(ygravity == 0):
        safetybouncecount = safetybouncecount + 1
    elif(ygravity == 2):
        safetybouncecount = 0
    else:
        print("Something might be wrong:\n\tygravity= ",ygravity,"\n\tsafteybc= ",safetybouncecount)
    
    if(safetybouncecount >= 20):
         yvelocity = -30
         
    yvelocity = yvelocity + ygravity    
    ball.y_position = ball.y_position + yvelocity #+ ygravity #reposition ball based on hit
    y = ball.y_position
    print("Ball velocity x: ", xvelocity)
    print("Ball velocity y: ", yvelocity)
    return(ball.y_position, safetybouncecount, yvelocity, y)
    
def checkOutofBounds(x, y, xvelocity, yvelocity):
    if (ball.y_position < 0):
        ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()
    return (ball.x_position, ball.y_position, xvelocity, yvelocity)
    
def checkGoal(x,z1,z2,y,xvelocity,yvelocity):
    if ball.x_position <= 40:
        z1 = scoring(z1)
        ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()
    if ball.x_position >= width-80:
        z2 = scoring(z2)
        ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()
    return (z1,z2,ball.x_position,ball.y_position,xvelocity, yvelocity)
    
def scoring(z):
    z = z+1
    print(z)
    return z    
    
def reset_to_center():
    (ball.x_position,ball.y_position) = ((width/2),0)
    xvelocity, yvelocity = 0,0
    time.sleep(0.01)
    return ball.x_position, ball.y_position, xvelocity, yvelocity

###################################################################################################################
targetScore = 5

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (topleft_x,topleft_y,head_width,head_height) in faces:
            center_x = int((2*topleft_x+head_width)/2)
            center_y = int((2*topleft_y+head_height)/2)
            head_radius = (head_width + head_height)/4
            cv2.circle(frame, (center_x,center_y), (int(head_radius)), (255,0,0), 2)#radius must be changed for different computers/different screens
            head_center = (center_x, center_y)
        
        Player_1.head_center = redefineHeadLocation(Player_1)
        Player_2.head_center = redefineHeadLocation(Player_2)
        
        if Player_1.hit(x,y):
            ball.x_position, xvelocity, headvelocity_x = xUpdate(Player_1,xvelocity,yvelocity)
            xvelocity = x_momentumconservation(Player_1,headvelocity_x,xvelocity)
            ball.x_position,xvelocity,x = final_x(xvelocity)
            
            ball.y_position, yvelocity, headvelocity_y = yUpdate(safetybouncecount,Player_1,xvelocity,yvelocity,headvelocity_y)
            yvelocity = y_momentumconservation(Player_1,headvelocity_y,yvelocity)
            ball.y_position, safetybouncecount,yvelocity,y = final_y(yvelocity,safetybouncecount)
            print("Ball Position @: ", ball.x_position,ball.y_position)
            ball.x_position, ball.y_position, xvelocity, yvelocity= checkOutofBounds(ball.x_position,ball.y_position, xvelocity,yvelocity)
            z1,z2,ball.x_position,ball.y_position,xvelocity,yvelocity = checkGoal(ball.x_position,z1,z2,ball.y_position,xvelocity,yvelocity)
        
        elif Player_2.hit(x,y):
            ball.x_position, xvelocity, headvelocity_x = xUpdate(Player_2)
            xvelocity = x_momentumconservation(Player_2,headvelocity_x,xvelocity)
            ball.x_position,xvelocity,x = final_x(xvelocity)
            
            ball.y_position, yvelocity, headvelocity_y = yUpdate(safetybouncecount,Player_2,xvelocity,yvelocity)
            yvelocity = y_momentumconservation(Player_2,headvelocity_y,yvelocity)
            ball.y_position, safetybouncecount,yvelocity,y = final_y(yvelocity,safetybouncecount)
            print("Ball Position @: ", ball.x_position,ball.y_position)        
            ball.x_position, ball.y_position, xvelocity, yvelocity= checkOutofBounds(ball.x_position,ball.y_position, xvelocity,yvelocity)
            z1,z2,ball.x_position,ball.y_position,xvelocity,yvelocity = checkGoal(ball.x_position,z1,z2,ball.y_position,xvelocity,yvelocity)
    
        else: # MAY NEED UNIQUE FUNCTION TO MAKE SURE THAT BALL IS ALWAYS MOVING WITH MOMENTUM EACH FRAME, SUSPICION IS THAT WITHOUT HEAD CONTACT THE FRAMES NEVER UPDATE.
            ball.x_position, xvelocity = xUpdate(None,xvelocity,yvelocity)
            ball.x_position,xvelocity,x = final_x(xvelocity)
            
            ball.y_position, yvelocity = yUpdate(safetybouncecount,None,xvelocity,yvelocity,headvelocity_y)
            ball.y_position, safetybouncecount,yvelocity,y = final_y(yvelocity,safetybouncecount)
            print("Ball Position @: ", ball.x_position,ball.y_position)
            ball.x_position, ball.y_position, xvelocity, yvelocity= checkOutofBounds(ball.x_position,ball.y_position, xvelocity,yvelocity)
            z1,z2,ball.x_position,ball.y_position,xvelocity,yvelocity = checkGoal(ball.x_position,z1,z2,ball.y_position,xvelocity,yvelocity)        
        
###############################################################################################################     
        print()
        print("Summary List: ")
        print("****************************************")
        
        #print("Head radius: ", head_radius)
        print("Head center x,y: ", head_center[0], head_center[1])
        print("Ball position x,y: ", Ball.x_position, Ball.y_position)
        print("Ball velocity x: ", xvelocity)
        print("Ball velocity y: ", yvelocity)

        #Creation of objects
       
        text1 = str("K: " + str(z1))#str(Player_1.name,": ", str(z1))
        print("text1: ", text1)
        text2 = str("J: " + str(z2))#str(Player_2.name,": ", + str(z2))  
        print("text2: ", text2)
################################################################################################################################################################################        
        cv2.circle(frame,(int(ball.x_position),int(ball.y_position)), 25, (150,150,0), -1)  #ball rad 25
        
        frame = cv2.flip(frame,1) 
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame,(40,50),(100,height-300),(0,0,255),3)
        cv2.putText(frame,text1,(60,height-400), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.rectangle(frame,(width-100,50),(width-40,height-300),(255,0,0),3)
        cv2.putText(frame,text2,(width-90,height-400), font, 0.5,(0,0,0),2,cv2.LINE_AA)
        
        cv2.line(frame,(40,0),(40,height),(0,0,255),20)
        cv2.line(frame,(width-40,0),(width-40,height),(255,0,0),20)
        cv2.line(frame,(0,height),(width,height),(255,0,255),40)
        
        if ((z1-z2) >= 2 and z1 >= targetScore):
            cv2.rectangle(frame,(150,100),(width-150,int(height/2)),(255,0,255),3)
            cv2.putText(frame, "K Wins!",(150,int(height/2) - 50), font, 3,(255,0,255),2,cv2.LINE_AA)#str(Player_1.name," Wins!"),(150,180), font, 3,(255,0,255),2,cv2.LINE_AA)
            ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()
        if ((z2-z1) >= 2 and z2 >= targetScore):
            cv2.rectangle(frame,(150,100),(width-150,int(height/2)),(0,255,0),3)
            cv2.putText(frame, "J Wins!",(150,int(height/2) - 50), font, 3,(0,255,0),2,cv2.LINE_AA)#str(Player_2.name," Wins!"),(150,180), font, 3,(0,255,0),2,cv2.LINE_AA)
            ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()       
        cv2.imshow('frame',frame)
        spacebar = cv2.waitKey(32) & 0xff
        if spacebar == 32:
            z1 = 0
            z2 = 0
            ball.x_position, ball.y_position, xvelocity, yvelocity = reset_to_center()
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()