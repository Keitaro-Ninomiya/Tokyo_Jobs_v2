import os, cv2, statistics
import numpy as np
def Split(n,HLine):
    with open(filepath+"\\Page"+str(n)+".pdf", "rb") as in_f:
        input1 = PdfReader(in_f)
        output = PdfWriter()

        numPages = len(input1.pages)
        print("document has %s pages." % numPages)
        
        #Left Page
        Page=2*n
        if not os.path.exists(savepath+"\\Page"+str(Page)):
            os.mkdir(savepath+"\\Page"+str(Page))
        for i in range(numPages):
            page = input1.pages[i]
            page.trimbox.lower_left = page.cropbox.lower_left
            page.trimbox.upper_right = (HLine, page.cropbox.upper_right[1])
            page.cropbox.lower_left = page.cropbox.lower_left
            page.cropbox.upper_right = (HLine, page.cropbox.upper_right[1])
            output.add_page(page)
        with open(savepath+"\\Page"+str(Page)+"\\Left.pdf", "wb") as out_f:
            output.write(out_f)
            
        #Right Page
        Page=2*n+1
        if not os.path.exists(savepath+"\\Page"+str(Page)):
            os.mkdir(savepath+"\\Page"+str(Page))
        for i in range(numPages):
            page = input1.pages[i]
            page.trimbox.lower_left = (HLine, page.cropbox.lower_left[1])
            page.trimbox.upper_right = page.cropbox.upper_right
            page.cropbox.lower_left = (HLine, page.cropbox.lower_left[1])
            page.cropbox.upper_right = page.cropbox.upper_right
            output.add_page(page)

        with open(savepath+"\\Page"+str(Page)+"\\Right.pdf", "wb") as out_f:
            output.write(out_f)
            

def HoriPart(path):
    '''
    Calculates the location of a line horizontally splitting a book into two pages.
    '''
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    HH,WW=img.shape[:2]
    img =img[0:HH,2*WW//5:3*WW//5]
    # Convert the image to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the edges in the image using canny detector
    edges = cv2.Canny(gray, 50, 200)
    # Detect points that form a line
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=200, maxLineGap=20)
    if len(lines)%2==1:
        Median=statistics.median([d[0][0].tolist() for d in lines if abs(d[0][0]-d[0][2])<5])
    if len(lines)%2==0:
        Median=statistics.median([d[0][0].tolist() for d in lines if abs(d[0][0]-d[0][2])<5]+[200])

    CenterLine=[d[0].tolist() for d in lines if d[0][0]==Median]
    
    CenterLine[0][0]=CenterLine[0][0]+2*WW//5
    CenterLine[0][2]=CenterLine[0][2]+2*WW//5
    return(CenterLine[0])

def VertPart(path):
    '''
    Calculates the location of a line vertically splitting a page into two pages.
    '''
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    HH,WW=img.shape[:2]
    img =img[3*HH//7:4*HH//7,0:WW]
    # Convert the image to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the edges in the image using canny detector
    edges = cv2.Canny(gray, 50, 200)
    # Detect points that form a line
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=200, maxLineGap=300)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        
    lines=[d for d in lines if abs(d[0][1]-d[0][3])<20]
    if len(lines)%2==1:
        Median=statistics.median([d[0][1].tolist() for d in lines])
    if len(lines)%2==0:
        lines=lines[1:]
        Median=statistics.median([d[0][1].tolist() for d in lines])

    CenterLine=[d[0].tolist() for d in lines if d[0][1]==Median]
    CenterLine[0][1]=CenterLine[0][1]+3*HH//7
    CenterLine[0][3]=CenterLine[0][3]+3*HH//7
    return(CenterLine[0])

def CheckLine(path,CenterLine):
    x1,y1,x2,y2=CenterLine
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    cv2.line(img,(x1,y1),(x2,y2),(225,0,0),2)
    cv2.imshow('',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
