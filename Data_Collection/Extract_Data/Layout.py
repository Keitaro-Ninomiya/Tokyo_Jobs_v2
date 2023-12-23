from statistics import mean, median
import numpy as np
import math, cv2
#- Input
#  1. Vertical/Horizontal line location.
#  2. Office Location.
#  3. Position Location.
#
# <br>
# 
#- Output
#  
#  Vertical Line
#
## Steps
#
#- Step 1: Use office location.
#
#  Check if office location is included in any of the lower quadrants.
#
#  
#  If yes, crop image by the vicinity (longer on the upside of word) of the line and apply Hough transformation to the image.
#
#  Test if solution is close to the vertical line of the previous page.
#
#- Step 2 (if office is not included in quadrant): Use position information.
#
#  Check if position location is included in any of the lower quadrants.
#
#  Use '書記', '技手' as predictor. Don't use '主事' because its used for position details.


import itertools
def RefineVert(img,LocList,PosiDict,VertPoint,HoriPoint):
    #Find offices in lower quadrant
    LowQuants=[d for d in LocList if (d['Box']['bounding_poly'].vertices[0].y>VertPoint)]
    if len(LowQuants)>0:
        NameLine=mean([d['Box']['bounding_poly'].vertices[0].y for d in LowQuants])
        Range={'Top':int(NameLine*0.9),'Btm':int(NameLine*1.05)}
        
        #Cut image and apply Hough Transformation
        HH,WW=img.shape[:2]
        crop=img[Range['Top']:Range['Btm'],HoriPoint:WW]
        
        gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        lines = cv2.HoughLinesP(edges, 1, math.pi/2, 2, None, 50, 1);
        
        NewVertPoint=lines[0][0][1]+Range['Top']
        return(NewVertPoint)

    #Find Positions in lower quadrant.
    CollapsePosiList=[]
    for Office in list(PosiDict.keys()):
        CollapseOffice=list(itertools.chain(*PosiDict[Office]))
        CollapsePosiList.append(CollapseOffice)
    CollapsePosiList=list(itertools.chain(*CollapsePosiList))

    try:    
        LowQuants=[d for d in CollapsePosiList if (d['Location'][1]>VertPoint)]
        if len(LowQuants)>0:
            NameLine=median([d['Location'][1] for d in LowQuants])
            Range={'Top':int(NameLine*0.9),'Btm':int(NameLine*1.05)}
            
            #Cut image and apply Hough Transformation
            HH,WW=img.shape[:2]
            crop=img[Range['Top']:Range['Btm'],0:WW]
            
            gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray,50,150,apertureSize = 3)
            lines = cv2.HoughLinesP(edges, 1, math.pi/2, 2, None, 50, 1);
            
            NewVertPoint=lines[0][0][1]+Range['Top']
        return(NewVertPoint)
    except:
        return(VertPoint)