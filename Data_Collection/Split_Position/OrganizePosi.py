def Filter(PosiList):
    Positions=[d['Position'] for d in PosiList]
    
    if '技師' in Positions:
        Loc=[d['Location'] for d in PosiList if d['Position']=='技師'][0]
        PosiList=[d for d in PosiList if Loc[1]*0.8<=d['Location'][1]<=Loc[1]*1.2]
        return(PosiList)
    if '書記' in Positions:
        Loc=[d['Location'] for d in PosiList if d['Position']=='書記'][0]
        PosiList=[d for d in PosiList if Loc[1]*0.8<=d['Location'][1]<=Loc[1]*1.2]
        return(PosiList)
    if '主事' in Positions:
        Loc=[d['Location'] for d in PosiList if d['Position']=='主事'][0]
        PosiList=[d for d in PosiList if Loc[1]*0.8<=d['Location'][1]<=Loc[1]*1.2]
        return(PosiList)
    else:
        return(PosiList)        


def Split(Box,ThresList):
    BoxList=[]
    if len(ThresList)==0:
        return([list([Box]),ThresList])
    for n in range(len(ThresList)):
        ThresX=ThresList[n]['X']
        NewBox=[d for d in Box if (d.bounding_poly.vertices[0].x>ThresX)]
        BoxList.append(NewBox)
        Box=[d for d in Box if (d.bounding_poly.vertices[0].x<ThresX)]
        if n ==len(ThresList)-1:
            BoxList.append(Box)
    return(list([BoxList,ThresList]))

def SplitClova(Box,ThresList):
    BoxList=[]
    if len(ThresList)==0:
        return([list([Box]),ThresList])
    for n in range(len(ThresList)):
        ThresX=ThresList[n]['X']
        NewBox=[d for d in Box if (d['boundingPoly']['vertices'][0]['x']>ThresX)]
        BoxList.append(NewBox)
        Box=[d for d in Box if (d['boundingPoly']['vertices'][0]['x']<ThresX)]
        if n ==len(ThresList)-1:
            BoxList.append(Box)
    return(list([BoxList,ThresList]))

def Crop(texts,HoriPoint,VertPoint,Dict,Page):
    URBox=[d for d in texts if (d.bounding_poly.vertices[0].y<VertPoint) and (d.bounding_poly.vertices[0].x>HoriPoint)]
    LRBox=[d for d in texts if (d.bounding_poly.vertices[0].y>VertPoint) and (d.bounding_poly.vertices[0].x>HoriPoint)]
    ULBox=[d for d in texts if (d.bounding_poly.vertices[0].y<VertPoint) and (d.bounding_poly.vertices[0].x<HoriPoint)]
    LLBox=[d for d in texts if (d.bounding_poly.vertices[0].y>VertPoint) and (d.bounding_poly.vertices[0].x<HoriPoint)]

    OfficeThresUR=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y<VertPoint) and (d['Box']['bounding_poly'].vertices[0].x>HoriPoint)]
    OfficeThresLR=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y>VertPoint) and (d['Box']['bounding_poly'].vertices[0].x>HoriPoint)]
    OfficeThresUL=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y<VertPoint) and (d['Box']['bounding_poly'].vertices[0].x<HoriPoint)]
    OfficeThresLL=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y>VertPoint) and (d['Box']['bounding_poly'].vertices[0].x<HoriPoint)]
    
    CroppedDict={'UR':{"Box":URBox,'Thres':OfficeThresUR},
             'LR':{"Box":LRBox,'Thres':OfficeThresLR},
             'UL':{"Box":ULBox,'Thres':OfficeThresUL},
             'LL':{"Box":LLBox,'Thres':OfficeThresLL}}
    return(CroppedDict)

def CropClova(texts,HoriPoint,VertPoint,Dict,Page):
    URBox=[d for d in texts if (d['boundingPoly']['vertices'][0]['y']<VertPoint) and (d['boundingPoly']['vertices'][0]['x']>HoriPoint)]
    LRBox=[d for d in texts if (d['boundingPoly']['vertices'][0]['y']>VertPoint) and (d['boundingPoly']['vertices'][0]['x']>HoriPoint)]
    ULBox=[d for d in texts if (d['boundingPoly']['vertices'][0]['y']<VertPoint) and (d['boundingPoly']['vertices'][0]['x']<HoriPoint)]
    LLBox=[d for d in texts if (d['boundingPoly']['vertices'][0]['y']>VertPoint) and (d['boundingPoly']['vertices'][0]['x']<HoriPoint)]

    OfficeThresUR=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y<VertPoint) and (d['Box']['bounding_poly'].vertices[0].x>HoriPoint)]
    OfficeThresLR=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y>VertPoint) and (d['Box']['bounding_poly'].vertices[0].x>HoriPoint)]
    OfficeThresUL=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y<VertPoint) and (d['Box']['bounding_poly'].vertices[0].x<HoriPoint)]
    OfficeThresLL=[{'Office':d['OfficeName'],'X':d['Box']['bounding_poly'].vertices[0].x} for d in Dict[Page] if (d['Box']['bounding_poly'].vertices[0].y>VertPoint) and (d['Box']['bounding_poly'].vertices[0].x<HoriPoint)]
    
    CroppedDict={'UR':{"Box":URBox,'Thres':OfficeThresUR},
             'LR':{"Box":LRBox,'Thres':OfficeThresLR},
             'UL':{"Box":ULBox,'Thres':OfficeThresUL},
             'LL':{"Box":LLBox,'Thres':OfficeThresLL}}
    return(CroppedDict)

