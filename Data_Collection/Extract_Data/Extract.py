import os,cv2,sys

def Center(PolyBox):
    ymax,ymin=min([d.y for d in PolyBox]),max([d.y for d in PolyBox])
    xmax,xmin=min([d.x for d in PolyBox]),max([d.x for d in PolyBox])
    return({'YCenter':(ymax+ymin)//2,'XCenter':(xmax+xmin)//2})

def ToDict(Box):
    Output={}
    Output['description']=Box.description
    Output['bounding_poly']=[d for d in Box.bounding_poly.vertices]
    Output['Center']=Center(Output['bounding_poly'])
    return(Output)

def AssignIndex(List):
    for n in range(len(List)):
        List[n]['ID']=n
    return(List)

def DetectCols(Box,TopLine,img):
    """
    Extracts data from text item after organizing them in table order.
    """
    copy=img.copy()
    Box=[ToDict(d) for d in Box]
    Box=AssignIndex(Box)
    
    i,ColDict=1,{}
    ColDict[str(i)]=[]
    TopRow=[d for d in Box if (TopLine+30>=d['Center']['YCenter']>=TopLine)]
    if len(TopRow)==0:
        TopLine=TopLine+100
        TopRow=[d for d in Box if (d['Center']['YCenter']<=TopLine)]
        if len(TopRow)==0:
            return([])
        

    for ColCell in TopRow:
        XCenter,YCenter=ColCell['Center']['XCenter'],ColCell['Center']['YCenter']
        cv2.line(copy,(XCenter,YCenter),(XCenter,YCenter),(225,0,0),4)        
    #Find Columns
    IDList=[]
    
    ##First Column
    RightLoc=max([d['Center']['XCenter'] for d in TopRow])
    Cell=[d for d in TopRow if d['Center']['XCenter']==RightLoc][0]
    ColDict[str(i)].append(Cell['description'])
    
    IDList.append(Cell['ID'])
    XCenter,YCenter=Cell['Center']['XCenter'],Cell['Center']['YCenter']
    cv2.line(copy,(XCenter,YCenter),(XCenter,YCenter),(0,225,0),4)
    #cv2.imshow('',copy)
    #cv2.waitKey(0)

    CandidateCells=[d for d in Box if (d['Center']['XCenter']>RightLoc-10) &(d['ID'] not in IDList)]
    
    while len(CandidateCells)>0:    
        NextY=min([d['Center']['YCenter'] for d in CandidateCells])
        Cell=[d for d in CandidateCells if d['Center']['YCenter']==NextY][0]
        ColDict[str(i)].append(Cell['description'])

        IDList.append(Cell['ID'])
        XCenter,YCenter=Cell['Center']['XCenter'],Cell['Center']['YCenter']
        cv2.line(copy,(XCenter,YCenter),(XCenter,YCenter),(0,225,0),4)
        #cv2.imshow('',copy)
        #cv2.waitKey(0)

        CandidateCells=[d for d in Box if (d['Center']['XCenter']>RightLoc-8) &(d['Center']['XCenter']<RightLoc+8) &(d['ID'] not in IDList)]
    #cv2.destroyAllWindows()
    
    Box=[d for d in Box if (d['ID'] not in IDList)]
    TopRow=[d for d in Box if(TopLine+80>=d['Center']['YCenter']>=TopLine)]
    i=i+1
    
    ##Remaining Columns
    while (len(TopRow)>0):        
        ColDict[str(i)]=[]
        RightLoc=max([d['Center']['XCenter'] for d in TopRow])
        Cell=[d for d in TopRow if d['Center']['XCenter']==RightLoc][0]
        ColDict[str(i)].append(Cell['description'])
        IDList.append(Cell['ID'])
        XCenter,YCenter=Cell['Center']['XCenter'],Cell['Center']['YCenter']
        cv2.line(copy,(XCenter,YCenter),(XCenter,YCenter),(0,225,0),4)
        
        #cv2.imshow('',copy)
        #cv2.waitKey(0)

        CandidateCells=[d for d in Box if (d['Center']['XCenter']>RightLoc-5) &(d['Center']['XCenter']<RightLoc+5) &(d['ID'] not in IDList)]

        while len(CandidateCells)>0:    
            NextY=min([d['Center']['YCenter'] for d in CandidateCells])
            Cell=[d for d in CandidateCells if d['Center']['YCenter']==NextY][0]
            ColDict[str(i)].append(Cell['description'])

            IDList.append(Cell['ID'])
            XCenter,YCenter=Cell['Center']['XCenter'],Cell['Center']['YCenter']
            cv2.line(copy,(XCenter,YCenter),(XCenter,YCenter),(0,225,0),4)
            #cv2.imshow('',copy)
            #cv2.waitKey(0)

            CandidateCells=[d for d in Box if (d['Center']['XCenter']>XCenter-8) &(d['Center']['XCenter']<XCenter+8) & (d['Center']['YCenter']>YCenter) &(d['ID'] not in IDList)]
        
        Box=[d for d in Box if (d['ID'] not in IDList)]
        TopRow=[d for d in Box if ((TopLine+30>=d['Center']['YCenter']>=TopLine))]
        i=i+1
    
    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resized_Window", 1280, 1440)
    cv2.imshow('Resized_Window',copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(ColDict)

def Test(Dict):
    if Dict=={}:
        Dict['Office']=list([{"Position":'NoPosition',"Location":[1500,100]}])
    return(Dict)

from OrganizeName import FilterPosi,RenewPosiList

def ExtractName(BoxList,OfficeList,PosiDict,HoriPoint,VertPoint,NameDict,NewQuant,OldQuant,img):        
    """
    Sequence for name/wage extraction.
    """
    if NewQuant=='UR':
        NewDict=FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuant)
        OldDict={'Pre':[{'Position':'PrePosi','Location':[100,100]}]}
    else:
        NewDict=FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuant)
        OldDict=FilterPosi(PosiDict,HoriPoint,VertPoint,OldQuant)
    
    NewDict,OldDict=Test(NewDict),Test(OldDict)
    
    for n in range(len(BoxList)):
        BoxOffice=BoxList[n]
        Office=OfficeList[n]
        
        PosiList=RenewPosiList(OldDict,NewDict)[Office]
        try:
            len(PosiList.keys())
            PosiList=list([PosiList])
        except:
            PosiList=sorted(PosiList, key=lambda x: x['Location'][0], reverse=True)

        NameDict[Office]={}
        for k in range(len(PosiList)):
            if k!=len(PosiList)-1:
                Posi=PosiList[k]['Position']
                RightX,LeftX=PosiList[k]['Location'][0],PosiList[k+1]['Location'][0]
                TopY=PosiList[k]['Location'][1]
                Box=[d for d in BoxOffice if (d.bounding_poly.vertices[0].x<=RightX)and(d.bounding_poly.vertices[0].x>LeftX)]
                NameDict[Office][Posi]=DetectCols(Box,TopY,img)
            if k==len(PosiList)-1:
                Posi=PosiList[k]['Position']
                RightX=PosiList[k]['Location'][0]
                TopY=PosiList[k]['Location'][1]
                Box=[d for d in BoxOffice if (d.bounding_poly.vertices[0].x<=RightX)]
                NameDict[Office][Posi]=DetectCols(Box,TopY,img)
    return(NameDict)

def CountSize(Office,NameDict):
    Data={}
    Data[Office]={}
    Dict=NameDict[Office]
    Positions=list(Dict.keys())
    for Posi in Positions:
        Data[Office][Posi]=len(NameDict[Office][Posi])
    Data=pd.DataFrame(Data).transpose()
    return(Data)
