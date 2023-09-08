import sys, cv2, os, statistics
sys.path.append('C:\\Users\\Keitaro Ninomiya\\Box\\Research Notes (keitaro2@illinois.edu)\\Tokyo_Jobs\\Data_Collection\\Extract_Data')
from Extract import ToDict
import numpy as np

def Gap(nums):
    nums.sort()
    max_gap = max(b-a for a, b in zip(nums, nums[1:]))
    
    MaxList=[list([a,b]) for a, b in zip(nums, nums[1:]) if b-a==max_gap][0]
    return(MaxList)

def GetCenter(Gap):
    x1,x2=Gap[0],Gap[1]
    return((x1+x2)//2)

def HoriPart(img,Page,texts):
    '''
    Calculates the location of a line horizontally splitting a book into two pages.
    '''
    try:
        HH,WW=img.shape[:2]
        Box=[ToDict(d) for d in texts][1:]
        CenterList=[d['Center']['XCenter'] for d in Box]
        Gap1=Gap(CenterList)

        HH,WW=img.shape[:2]
        img =img[0:HH,Gap1[0]:Gap1[1]]

        # Convert the image to gray-scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the edges in the image using canny detector
        edges = cv2.Canny(gray, 50, 200)

        # Detect points that form a line
        lines = [d[0] for d in cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=20)]

        if len(lines)%2==1:
            Median=statistics.median([d[0].tolist() for d in lines if abs(d[0]-d[2])<5])
        if len(lines)%2==0:
            Median=statistics.median([d[0].tolist() for d in lines if abs(d[0]-d[2])<5]+[0])

        CenterLine=[d.tolist() for d in lines if d[0]==Median][0]

        CenterLine[0]=CenterLine[0]+Gap1[0]
        CenterLine[2]=CenterLine[2]+Gap1[0]
        if (CenterLine[0]>=2*WW//3) or (CenterLine[0]<=WW//3):
            texts=[d for d in texts if WW//3<=d.bounding_poly.vertices[0].x<=2*WW//3]
            Box=[ToDict(d) for d in texts][1:]
            CenterList=[d['Center']['XCenter'] for d in Box]
            Gap1=Gap(CenterList)
    
            HH,WW=img.shape[:2]
            img =img[0:HH,Gap1[0]:Gap1[1]]
    
            # Convert the image to gray-scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the edges in the image using canny detector
            edges = cv2.Canny(gray, 50, 200)
    
            # Detect points that form a line
            lines = [d[0] for d in cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=20)]
    
            if len(lines)%2==1:
                Median=statistics.median([d[0].tolist() for d in lines if abs(d[0]-d[2])<5])
            if len(lines)%2==0:
                Median=statistics.median([d[0].tolist() for d in lines if abs(d[0]-d[2])<5]+[0])
    
            CenterLine=[d.tolist() for d in lines if d[0]==Median][0]
    
            CenterLine[0]=CenterLine[0]+Gap1[0]
            CenterLine[2]=CenterLine[2]+Gap1[0]
        return(CenterLine)
    except:
        print('Horizontal Line was not automatically detected... Defining line arbitrariry...')
        return([(Gap1[0]+Gap1[1])//2,0,(Gap1[0]+Gap1[1])//2,HH])