import cv2

def Show(img,LocList):
    copy=img.copy()
    HH,WW=copy.shape[:2]
    for Office in LocList:
        OfficeName=Office['OfficeName']
        XLine=Office['Box']['bounding_poly'].vertices[1].x
        cv2.line(copy,(XLine,0),(XLine,HH),(0,0,0),3)
    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resized_Window", 1280, 1440)
    cv2.imshow('Resized_Window',copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()