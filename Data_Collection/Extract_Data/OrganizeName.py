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


import pandas as pd
def Convert2(PageNum,Office,Posi,Table,Names):
    Data=pd.DataFrame(columns=['Page','Office','Posi','Name','Total'])
    Total=len(Table)
    if Posi in list(['書記','技手']):
        for Name in Names:        
            NewData=pd.DataFrame({'Page':[PageNum],'Office':[Office],'Posi':Posi,'Name':[Name],'Total':2*Total})            
            Data=pd.concat([Data,NewData])
    
    if Posi =='雇':
        for Name in Names:        
            NewData=pd.DataFrame({'Page':[PageNum],'Office':[Office],'Posi':Posi,'Name':[Name],'Total':3*Total})            
            Data=pd.concat([Data,NewData])
    
    if Posi in list(['主事','技師']):
        for Name in Names:        
            NewData=pd.DataFrame({'Page':[PageNum],'Office':[Office],'Posi':Posi,'Name':[Name],'Total':1*Total})            
            Data=pd.concat([Data,NewData])
            
    return(Data)

def Convert(PageNum,Office,Posi,Page,Table,Names):
    Data=pd.DataFrame(columns=['Page','Office','Posi','Name','Total'])
    Total=len(Table)
    if Posi in list(['書記','技手']):
        for Line in Table:
            LineNum=list(Line.keys())[0]
            Wage1=''.join([d['description'] for d in Line[PageNum]['Wage1']])
            Name1=''.join([d['description'] for d in Line[PageNum]['Name1']])
            Data1=pd.DataFrame({'Page':[Page],'Office':[Office],'Posi':Posi,'Name':[Name1],'Wage':[Wage1],'Total':2*Total})
            
            Wage2=''.join([d['description'] for d in Line[PageNum]['Wage2']])
            Name2=''.join([d['description'] for d in Line[PageNum]['Name2']])
            Data2=pd.DataFrame({'Page':[Page],'Office':Office,'Posi':Posi,'Name':[Name2],'Wage':[Wage2],'Total':2*Total})
            
            Data=pd.concat([Data,Data1,Data2])
    
    if Posi =='雇':
        for Line in Table:
            PageNum=list(Line.keys())[0]
            Name1=''.join([d['description'] for d in Line[PageNum]['Name1']])
            Data1=pd.DataFrame({'Page':[Page],'Office':[Office],'Posi':[Posi],'Name':[Name1],'Wage':['NA'],'Total':3*Total})
            
            Name2=''.join([d['description'] for d in Line[PageNum]['Name2']])
            Data2=pd.DataFrame({'Page':[Page],'Office':[Office],'Posi':[Posi],'Name':[Name2],'Wage':['NA'],'Total':3*Total})
    
            Name3=''.join([d['description'] for d in Line[PageNum]['Name3']])
            Data3=pd.DataFrame({'Page':[Page],'Office':[Office],'Posi':[Posi],'Name':[Name3],'Wage':['NA'],'Total':3*Total})
    
            Data=pd.concat([Data,Data1,Data2,Data3])
    
    if Posi in list(['主事','技師']):
        for Line in Table:
            PageNum=list(Line.keys())[0]
            Wage1=''.join([d['description'] for d in Line[PageNum]['Wage1']])
            Name1=''.join([d['description'] for d in Line[PageNum]['Name1']])
            Data1=pd.DataFrame({'Page':[Page],'Office':[Office],'Posi':Posi,'Name':[Name1],'Wage':[Wage1],'Total':Total})
    
            Data=pd.concat([Data,Data1])
    return(Data)