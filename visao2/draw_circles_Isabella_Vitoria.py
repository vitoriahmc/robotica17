#!/usr/bin/env python
__author__      = "Matheus Dib, Fabio de Miranda"


import cv2
#import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
import time
kernel = np.ones((5,5), np.uint8)
# If you want to open a video, just change this path
#cap = cv2.VideoCapture('hall_box_battery.mp4')

# Parameters to use when opening the webcam.
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lower = 0
upper = 1

# Returns an image containing the borders of the image
# sigma is how far from the median we are setting the thresholds
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged



while(True):
    # Capture frame-by-frame
    #print("New frame")
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # A gaussian blur to get rid of the noise in the image
    blur = cv2.GaussianBlur(gray,(5,5),25)
    # Detect the edges present in the image
    bordas = auto_canny(blur)
    

    circles = []


    # Obtains a version of the edges image where we can draw in color
    bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)

    # HoughCircles - detects circles using the Hough Method. For an explanation of
    # param1 and param2 please see an explanation here http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
    circles=cv2.HoughCircles(bordas,cv2.HOUGH_GRADIENT,2,40,param1=500,param2=130,minRadius=10,maxRadius=80)
    if circles != None:
        circles = np.uint16(np.around(circles))
        
        x_circle = []
        y_circle = []
        raios = []
        
        for i in circles[0,:]:
            # draw the outer circle
            # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            opening = cv2.morphologyEx(circles, cv2.MORPH_OPEN, kernel)
            cv2.circle(bordas_color,(i[0],i[1]),i[2],(0,255,0),2)
            x_circle.append(i[0])
            y_circle.append(i[1])
            raios.append(i[2])
            
            # draw the center of the circle
            cv2.circle(bordas_color,(i[0],i[1]),2,(0,0,255),3)
            
            if (len(raios)==3): #só começa quando houverem 3 circulos na tela
                dif_raio = max(raios)-min(raios)
                if dif_raio <= 1: #consideramos uma tolerância de até 1 cm no tamanho entre os raios dos círculos                
                    #printa a distancia entre a folha e a camera do computador
                    dist = (649*3.2/i[2])
                    print("Distância da tela:", ("%.2f" % dist), "cm")
                    #calcula as distância entre os centros nos eixos x e y                
                    eixo_x = (max(x_circle)-min(x_circle))
                    eixo_y = (max(y_circle)-min(y_circle))

                    #se a distancia entre os centros em x for maior que a distancia em y os circulos estão na horizontal
                    if eixo_x >= eixo_y:
                        print("Horizontal")
                    else:
                        print("Vertical")
            
            
    # Draw a diagonal blue line with thickness of 5 px
    # cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    #cv2.line(bordas_color,(0,0),(511,511),(255,0,0),5)

    # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    #cv2.rectangle(bordas_color,(384,0),(510,128),(0,255,0),3)

    # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(bordas_color,'Ninjutsu ;)',(0,50), font, 2,(255,255,255),2)
    cv2.putText(bordas_color,'Por: Vitoria e Isabella',(280,450), font, 1,(255,255,255),1)

    #More drawing functions @ http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html

    # Display the resulting frame
    cv2.imshow('Detector de circulos',bordas_color)
    #print("No circles were found")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
