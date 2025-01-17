import cv2
import cvzone

from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture("video2.mp4")
detector = FaceMeshDetector()
plotY = LivePlot(540,360,[10,60])


idList = [22,23,24,26,110,157,158,159,160,161,130,243]
color = (0,0,255)
ratioList = []
counter = 0
blinkCounter =0
while True:
    success , img = cap.read()
    if success:
        img, faces = detector.findFaceMesh(img, draw=False)
        if faces:
           face = faces[0]
           for id in idList:
               cv2.circle(img,face[id],5,color, cv2.FILLED)
            
           leftUp = face[159]
           leftDown = face[23]
           leftLeft = face[130]
           leftRight = face[243]
           
           lenghtVer,_ = detector.findDistance(leftUp, leftDown)
           lenghtHor,_ = detector.findDistance(leftLeft, leftRight)
            
           cv2.line(img,leftUp, leftDown, (0,255,0),3)
           cv2.line(img,leftLeft, leftRight, (255,0,0),3)
           
           
           ratio = int((lenghtVer/lenghtHor)*100)
           ratioList.append(ratio)
           
           ratioAvg = sum(ratioList)/len(ratioList)
           if len(ratioList) > 3:
               ratioList.pop(0)
           
           if ratioAvg <35 and counter ==0:
               blinkCounter+=1
               counter=1
               color = (0,255,0)
           if counter != 0:
               counter+=1
               if counter > 10:
                   counter = 0
                   color = (0,0,255)
                   
           cvzone.putTextRect(img,f"Blink count : {blinkCounter}", (50,100), colorR=color)
           
           
           
           imgPlot = plotY.update(ratioAvg,color)
           img = cv2.resize(img, (640,360))
           imgStack = cvzone.stackImages([img,imgPlot],2,1)
           
           
    else: break
    
    




    cv2.imshow("img",imgStack)
    k = cv2.waitKey(17) & 0xFF
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()



cap.release()
cv2.destroyAllWindows()