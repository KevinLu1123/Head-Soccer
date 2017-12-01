# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10:27:10 2017

@author: Kevin Lu
"""

#import numpy as np
import cv2
import math

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if(ret == False):
    cap = cv2.VideoCapture(0)
width = int(cap.get(3))  # float
height = int(cap.get(4)) # float

z1 = 0
z2 = 0
xvelocity = 0
yvelocity = 0
coefficientFactor = 0
head_center = (int(width/2),int(height/2))
prev_x = head_center[0]
prev_y = head_center[1]
x = width/2
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
    x_position = x
    y_position = y
    def boundary (y, yvelocity, coefficientFactor):
        if y >= height - 30:
            coefficientFactor = coefficientFactor + 1
            yvelocity = -yvelocity * (0.9**coefficientFactor)
        return yvelocity, coefficientFactor

def velocityx(x, head_center, xvelocity):
    global prev_x
    headvelocity_x = head_center[0] - prev_x
    prev_x = head_center[0]
    xvelocity = -1*int(Player.headmass/Ball.mass) * headvelocity_x
    return (headvelocity_x, prev_x, xvelocity)

def velocityy(y, head_center, yvelocity):
    global prev_y
    headvelocity_y = head_center[1] - prev_y
    prev_y = head_center[1]
    yvelocity = int(Player.headmass/Ball.mass) * headvelocity_y
    return (headvelocity_y, prev_y, yvelocity)

def hit(x, y, head_center):
    hit_criteria = head_radius + 25
    distanceheadball = math.sqrt((head_center[0]-ball.x_position)**2 + (head_center[1]-ball.y_position)**2)
    eta = 0.000001
    if(hit_criteria >= distanceheadball):# IF this is a hit, then proceed to implement velocity functions
        global slope, xvelocity, yvelocity
        slope = int((ball.y_position - center_y)/(ball.x_position - center_x + eta))
        _, _, xvelocity = velocityx(x,head_center,xvelocity)#Determining the x and y velocities of the ball
        _, _, yvelocity = velocityy(y,head_center,yvelocity)
    print("HIT: ", hit_criteria >= distanceheadball)
    print("radii sum: ", hit_criteria)
    print("distance between head and ball centers: ", distanceheadball)
    return(slope,x,y,xvelocity,yvelocity)   
    
def xUpdate(x,):
    _, ball.x_position, _, xvelocity, _ = hit(ball.x_position,ball.y_position,head_center)#call function for if head hits ball
    ball.x_position = ball.x_position + xvelocity #reposition ball based on the hit
    return(ball.x_position,xvelocity)
def yUpdate(y,flag):
    global yvelocity, coefficientFactor
    _, _, ball.y_position, _, yvelocity = hit(ball.x_position,ball.y_position,head_center)
    #ygravity = 2 + int((t**2)/32)
    ygravity = 4
    ball.y_position = ball.y_position + yvelocity + ygravity
    yvelocity,coefficientFactor = Ball.boundary(ball.y_position, yvelocity,coefficientFactor) # flip direction in the event of a bounce
    if ball.y_position >= 450:
        ball.y_position = 450 + yvelocity + ygravity
    #else:
    #    y = y + yvelocity + ygravity #reposition ball based on hit
    return(ball.y_position)
  
    # JAMES BOUNCE VERSION - REMOVE T
#    if y > 450:
#        y = 480
#        yvelocity = int(-1 * math.sqrt(2*2*y) * (0.9**coefficientFactor))
#        print("yvelocity" , yvelocity , "\n")
#        constant = 625
#        coefficientFactor = coefficientFactor+1
#    y = ( int(yvelocity*t) + int( (t**2) ) + constant)
#    print("yupdate" , y , "\n\t yvelocity*t = ",(yvelocity*t),"\n\t t^2 = ",(t**2),"\n\t c = ",constant,"\n")
    
    #print (y)
#    return(t,y,yvelocity,constant,coefficientFactor)

def checkGoal(x,z1,z2,y,xvelocity,yvelocity):
    if ball.x_position <= 40:
        z1 = scoring(z1,flag)
        ball.x_position = width/2
        ball.y_position = 0
        xvelocity = 0
        yvelocity = 0
    if ball.x_position >= width-80:
        z2 = scoring(z2,flag)
        ball.x_position = width/2
        ball.y_position = 0
        xvelocity = 0
        yvelocity = 0
    return (z1,z2,ball.x_position,ball.y_position,xvelocity, yvelocity)
def scoring(z,flag):
    z = z+1
    print(z)
    return z    
def reset_to_center():
    (ball.x_position,ball.y_position) = (width/2),0
    xvelocity = 0
    yvelocity = 0
    headvelocity_x,headvelocity_y = 0,0
    coefficientFactor = 0
    return ball.x_position, ball.y_position, xvelocity, yvelocity, headvelocity_x, headvelocity_y, coefficientFactor

flag = True
targetScore = 5

Player_1 = Player()#"Kevin",140)#Give stats of players
Player_2 = Player()#"James",140)
ball = Ball()

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
            
        ball.x_position,xvelocity = xUpdate(ball.x_position)
        z1,z2,ball.x_position,ball.y_position,xvelocity,yvelocity = checkGoal(ball.x_position,z1,z2,ball.y_position,xvelocity,yvelocity)
        ball.y_position = yUpdate(ball.y_position,flag)
        
        print()
        print("Summary List: ")
        print("****************************************")
        
        print("Head radius: ", head_radius)
        print("Head center x,y: ", head_center[0], head_center[1])
        print("Ball position x,y: ", ball.x_position, ball.y_position)
        print("Ball velocity x: ", xvelocity)
        print("Ball velocity y: ", yvelocity)
        print("Coefficient Factor: ", coefficientFactor)
        print("Player 1: ",z1)
        print("Player 2: ",z2)
        print("Position: ({},{}) ".format(ball.x_position, ball.y_position))
        #Creation of objects
       
        text1 = str("K: " + str(z1))#str(Player_1.name,": ", str(z1))
        print("text1: ", text1)
        text2 = str("J: " + str(z2))#str(Player_2.name,": ", + str(z2))  
        print("text2: ", text2)
        
        cv2.circle(frame,(int(ball.x_position),int(ball.y_position)), 25, (150,150,0), -1)  
        
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
            flag = False
            cv2.rectangle(frame,(150,100),(width-150,int(height/2)),(255,0,255),3)
            cv2.putText(frame, "K Wins!",(150,int(height/2) - 50), font, 3,(255,0,255),2,cv2.LINE_AA)#str(Player_1.name," Wins!"),(150,180), font, 3,(255,0,255),2,cv2.LINE_AA)
            ball.x_position, ball.y_position, xvelocity, yvelocity, headvelocity_x, headvelocity_y, coefficientFactor = reset_to_center()
        if ((z2-z1) >= 2 and z2 >= targetScore):
            flag = False
            cv2.rectangle(frame,(150,100),(width-150,int(height/2)),(0,255,0),3)
            cv2.putText(frame, "J Wins!",(150,int(height/2) - 50), font, 3,(0,255,0),2,cv2.LINE_AA)#str(Player_2.name," Wins!"),(150,180), font, 3,(0,255,0),2,cv2.LINE_AA)
            ball.x_position, ball.y_position, xvelocity, yvelocity, headvelocity_x, headvelocity_y, coefficientFactor = reset_to_center()       
          
        cv2.imshow('frame',frame)
        spacebar = cv2.waitKey(32) & 0xff
        if spacebar == 32:
            z1 = 0
            z2 = 0
            ball.x_position, ball.y_position, xvelocity, yvelocity, headvelocity_x, headvelocity_y, coefficientFactor = reset_to_center()
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()