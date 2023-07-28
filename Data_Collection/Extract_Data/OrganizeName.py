def FilterPosi(PosiDict,HoriPoint,VertPoint,Quadrant):
    """
    Extract a dictionary of positions included in a quadrant.
    """
    FinDict={}

    if Quadrant=='UR':        
        for Office in PosiDict:    
            TempDict=PosiDict[Office]
            TempDict=[d for d in TempDict if (d['Location'][1]<VertPoint) & (d['Location'][0]>HoriPoint)]

            if len(TempDict)>=1:
                FinDict[Office]=TempDict
        return(FinDict)
    
    if Quadrant=='LR':        
        for Office in PosiDict:    
            TempDict=PosiDict[Office]
            TempDict=[d for d in TempDict if (d['Location'][1]>VertPoint) & (d['Location'][0]>HoriPoint)]

            if len(TempDict)>=1:
                FinDict[Office]=TempDict
        return(FinDict)

    if Quadrant=='UL':        
        for Office in PosiDict:    
            TempDict=PosiDict[Office]
            TempDict=[d for d in TempDict if (d['Location'][1]<VertPoint) & (d['Location'][0]<HoriPoint)]

            if len(TempDict)>=1:
                FinDict[Office]=TempDict
        return(FinDict)
    
    if Quadrant=='LL':        
        for Office in PosiDict:    
            TempDict=PosiDict[Office]
            TempDict=[d for d in TempDict if (d['Location'][1]>VertPoint) & (d['Location'][0]<HoriPoint)]

            if len(TempDict)>=1:
                FinDict[Office]=TempDict
        return(FinDict)
    
def RenewPosiList(OldDict,NewDict):
    """
    Add positions information from preceeding quadrant.
    """
    OldOffice=list(OldDict.keys())[-1]
    OldPosi=OldDict[OldOffice][-1]['Position']
    NewOffice=list(NewDict.keys())[0]
    if NewOffice!=OldOffice:
        NewDict[NewOffice][0]
        NewPosi,NewLocY=NewDict[NewOffice][0]['Position'],NewDict[NewOffice][0]['Location'][1]
        NewDict[OldOffice]={'Position':NewPosi,"Location":[1500,NewLocY]}
    if NewOffice==OldOffice:
        NewPosi,NewLocY=NewDict[NewOffice][0]['Position'],NewDict[NewOffice][0]['Location'][1]
        NewDict[OldOffice].append({'Position':OldPosi,"Location":[1500,NewLocY]})
    return (NewDict)

def GetOffice(NewQuad,OldQuad,PosiDict,HoriPoint,VertPoint):
    '''
    Gets list of offices for positions included in a quadrant
    '''
    if NewQuad=='UR':
        OfficeList=list(['Pre'])+list(FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuad).keys())
    else:
        OldDict,NewDict=FilterPosi(PosiDict,HoriPoint,VertPoint,OldQuad),FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuad)
        OldDict,NewDict=Test(OldDict),Test(NewDict)
        OfficeList=list(OldDict.keys())[-1:]+list(NewDict.keys())
    return(OfficeList)

def Test(Dict):
    if Dict=={}:
        Dict['Office']=list([{"Position":'NoPosition',"Location":[1500,100]}])
    return(Dict)