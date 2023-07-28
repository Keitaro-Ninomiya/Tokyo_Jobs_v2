import cv2,itertools

#Show 
def Show(PosiDict,Office,img,VertPoint,HoriPoint):
    copy=img.copy()
    HH,WW=copy.shape[:2]
    copy=img.copy()
    HH,WW=copy.shape[:2]
    cv2.line(copy,(HoriPoint,0),(HoriPoint,HH),(0,0,0),2)

    PosiList=list(itertools.chain(*FinalPosiDict[Office]))
    for Posi in PosiList:
        XAxis,YAxis=Posi['Location'][0],Posi['Location'][1]
        if YAxis<VertPoint:
            cv2.line(copy,(XAxis,0),(XAxis,VertPoint),(0,0,0),2)
        else:
            cv2.line(copy,(XAxis,VertPoint),(XAxis,HH),(0,0,0),2)    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resized_Window", 1280, 1440)
    cv2.imshow('Resized_Window',copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()