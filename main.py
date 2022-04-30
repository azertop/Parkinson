#!/usr/bin/env python
# -*- coding:Utf-8 -*-
import matplotlib
import cv2
import mediapipe as mp
import numpy as np
import keyboard as kb
import matplotlib.pyplot as plt
import time

class HandDetector() :
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5) :
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self,img,handNo=0,draw=False):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)   
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,handLms in enumerate(myHand.landmark) :
                if draw :
                    self.mpDraw.draw_landmarks(img,myHand,self.mpHands.HAND_CONNECTIONS)
        return img
                
    def findPosition(self,img,handNo=0,draw=False):
        lmList = []
        if self.results.multi_hand_landmarks :
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark) : 
                        h,w,c = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        lmList.append(np.array((cx,cy)))
                        #print(id,cx,cy)
                        if draw:
                            self.mpDraw.draw_landmarks(img,myHand,self.mpHands.HAND_CONNECTIONS)
                            cv2.circle(img,(cx,cy),10,(0,0,255),cv2.FILLED)
                    
        return lmList
    
    def ecart(self, img) :
        if self.results.multi_hand_landmarks :
            lmList1 = self.findPosition(img)[4]
            lmList2 = self.findPosition(img)[8]
            return np.linalg.norm(lmList1-lmList2)

def mise_en_route():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True :
        succes,img = cap.read()
        img = detector.findHands(img)
        cv2.line(img,(0,70),(1800,70),(0,0,255),6)
        cv2.putText(img,"Placez le haut de la main au dessus de la ligne",(50,60),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
        cv2.imshow("image",img)
        cv2.waitKey(1)
        if len(detector.findPosition(img))!=0 :
            if 70 > detector.findPosition(img)[0][1]:
                break
                    
def main():
    #mise_en_route()
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    pos = [np.array((0,0))]
    dist = [0] 
    temps=[]
    cTime = time.time()  
    while True :
        succes,img = cap.read()
        img = detector.findHands(img)
        if len(detector.findPosition(img))!=0 :
            pos.append(detector.findPosition(img))
            dist.append((np.linalg.norm(pos[-1][0]-pos[-2][0])))
            temps.append(time.time()-cTime)
        cv2.putText(img,"Le tremblement en pixel : "+str(dist[-1]),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
        cv2.imshow("image",img)
        cv2.waitKey(1)
        if kb.is_pressed('q'):
            break
    return dist,temps
      

def main3():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    pos = [np.array((0,0))]
    dist = [0] 
    temps=[]
    cTime = time.time()  
    while True :
        succes,img = cap.read()
        img = detector.findHands(img,draw=False)
        ecart = 0
        cv2.rectangle(img,(5,700),(50,350),(255,255,255),cv2.FILLED)
        if len(detector.findPosition(img))!=0:
            ecart = int(700-min(detector.ecart(img),350))
            cv2.rectangle(img,(5,700),(50,ecart),(0,0,0),cv2.FILLED)
        cv2.putText(img,str(int((700-ecart)*100/350)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
        cv2.imshow("image",img)
        cv2.waitKey(1)


#main3()
dist, temps = main()
dist.pop(0)
dist.pop(0)
temps.pop(0)
plt.figure()
plt.plot(temps,dist)
plt.xlabel("Temps en ms")
plt.ylabel("Déplacement en pixels")
plt.savefig('main.png')
