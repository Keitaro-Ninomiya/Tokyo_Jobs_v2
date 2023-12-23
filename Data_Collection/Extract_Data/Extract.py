import os,cv2,sys
import json

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


def Test(Dict):
    if Dict=={}:
        Dict['Office']=list([{"Position":'NoPosition',"Location":[1500,100]}])
    return(Dict)

from OrganizeName import FilterPosi,RenewPosiList

def CountSize(Office,NameDict):
    import pandas as pd
    Data={}
    Data[Office]={}
    Dict=NameDict[Office]
    Positions=list(Dict.keys())
    for Posi in Positions:
        Data[Office][Posi]=len(NameDict[Office][Posi])
    Data=pd.DataFrame(Data).transpose()
    return(Data)


def ExtractName(DF,PosiDict,HoriPoint,VertPoint,NewQuant,OldQuant,img,project,origin,Year,Page):
    Data={}
    
    #############################
    if NewQuant=='UR':
        NewDict=FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuant)
        OldDict={'Pre':[{'Position':'PrePosi','Location':[100,100]}]}
    else:
        NewDict=FilterPosi(PosiDict,HoriPoint,VertPoint,NewQuant)
        OldDict=FilterPosi(PosiDict,HoriPoint,VertPoint,OldQuant)
    ##############################


    QuadrantPosi=AggregatePosiList(NewDict,OldDict,HoriPoint,NewQuant)
    for n in range(len(QuadrantPosi)):
        OfficeEnd=GetOfficeEnd(DF,NewQuant,n,HoriPoint)

        OfficeList=[d[0] for d in QuadrantPosi.items()]
        Office=OfficeList[n]
        Data[Office]={}
        
        FinalQuadrantPosi=sorted(QuadrantPosi[Office],key=lambda e: e['Location'][0],reverse=True)
        for k in range(len(FinalQuadrantPosi)):
            Posi=FinalQuadrantPosi[k]
            Index,Position=k,Posi['Position']
            TopY=Posi['Location'][1]
            NewTopY=TopY
            Data[Office][Position]=[]
            
            copy=img.copy()
            
            if Index<len(FinalQuadrantPosi)-1:
                RightX=Posi['Location'][0]
                LeftX =FinalQuadrantPosi[Index+1]['Location'][0]
                if project=='On':                
                    cv2.line(copy,(RightX,0),(RightX,2000),(225,0,0),2)
                    cv2.line(copy,(LeftX,0),(LeftX,2000),(225,0,0),2)
                    cv2.line(copy,(LeftX,VertPoint),(RightX,VertPoint),(225,0,0),2)
                    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Resized_Window", 1280, 1440)    
                    cv2.imshow('Resized_Window',copy)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                
                Box=[ToDict(d) for d in DF[NewQuant]['Box']]
                Box=[d for d in Box if (LeftX<=d['bounding_poly'][1].x<=RightX)and(Position not in d['description'])]
            
                TopRow=[d for d in Box if (NewTopY*1.05>=d['Center']['YCenter']>=TopY)]
                while len(TopRow)==0:
                    NewTopY=NewTopY*1.05
                    TopRow=[d for d in Box if (NewTopY>=d['Center']['YCenter']>=TopY)]
                    if NewTopY>3*TopY:
                        TopRow=[]
                        break
                if TopRow==[]:
                    print('Failed to detect top rows')
                try:
                    NamesNDL=CountDataNDL(Index,OfficeEnd,FinalQuadrantPosi,HoriPoint,VertPoint,RightX,LeftX,origin,Year,Page,NewQuant)
                    Table=CountData(TopRow,Box,Posi['Position'])
                    Data[Office][Posi['Position']].append({'Table':Table,'Names':NamesNDL})
                except:
                    print('Failed to find tables')
                    
            if Index==len(FinalQuadrantPosi)-1:
                RightX=Posi['Location'][0]
                if project=='On':                 
                    cv2.line(copy,(RightX,0),(RightX,2000),(225,0,0),2)
                    cv2.line(copy,(0,VertPoint),(RightX,VertPoint),(225,0,0),2)
                    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Resized_Window", 1280, 1440)    
                    cv2.imshow('Resized_Window',copy)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                
                Box=[ToDict(d) for d in DF[NewQuant]['Box']]
                Box=[d for d in Box if (d['bounding_poly'][1].x<=RightX)and(Position not in d['description'])]
            
                TopRow=[d for d in Box if (NewTopY*1.05>=d['Center']['YCenter']>=TopY)]
                while len(TopRow)==0:
                    NewTopY=NewTopY*1.05
                    TopRow=[d for d in Box if (NewTopY>=d['Center']['YCenter']>=TopY)]
                    if NewTopY>3*TopY:
                        TopRow=[]
                        break
                if TopRow==[]:
                    print('Failed to detect top rows')
            
                try:
                    NamesNDL=CountDataNDL(Index,OfficeEnd,FinalQuadrantPosi,HoriPoint,VertPoint,RightX,LeftX,origin,Year,Page,NewQuant)
                    Table=CountData(TopRow,Box,Posi['Position'])
                    Data[Office][Posi['Position']].append({'Table':Table,'Names':NamesNDL})
                except:
                    print('Failed to find tables')
    return(Data)

def AggregatePosiList(NewDict,OldDict,HoriPoint,NewQuant):
    #Test for Office existence
    if len(OldDict)==0:
        OldOffice='Pre'
    else:
        OldOffice=list(OldDict.keys())[-1]
    
    ##Create list for last office in previous quadrant.
    if len(NewDict)==0:
        NewOffice=OldOffice
    else:
        NewOffice=list(NewDict.keys())[0]
    if OldOffice not in list(NewDict.keys()):
        NewDict[OldOffice]=[]
    
    #Add Position
    if len(OldDict)==0:
        OldPosition='PrePosi'
    else:
        OldPosition=sorted(OldDict[OldOffice],key=lambda e: e['Location'][0],reverse=True)[-1]['Position']
    if len(NewDict[NewOffice])==0:
        NewPositionY=500
    else:
        NewPositionY=sorted(NewDict[NewOffice],key=lambda e: e['Location'][0],reverse=True)[0]['Location'][1]
    
    if NewQuant in list(['UR','LR']):
        NewDict[OldOffice].insert(0,{'Position':OldPosition,'Location':[3000,NewPositionY]})
    else:
        NewDict[OldOffice].insert(0,{'Position':OldPosition,'Location':[HoriPoint,NewPositionY]})
    return(NewDict)

def GetOfficeEnd(DF,NewQuant,n,HoriPoint):
    OfficeThresList=sorted([d['X'] for d in DF[NewQuant]['Thres']],reverse=True)
    if  len(DF[NewQuant]['Thres'])==0:
        if NewQuant in list(['UL','LL']):        
            OfficeEnd=0
        elif NewQuant in list(['UR','LR']):
            OfficeEnd=HoriPoint
            
    elif len(DF[NewQuant]['Thres'])==1:
        if n<1:
            OfficeEnd=OfficeThresList[n]
        else:
            if NewQuant in list(['UL','LL']):        
                OfficeEnd=0
            elif NewQuant in list(['UR','LR']):
                OfficeEnd=HoriPoint        
    else:
        if n< len(DF[NewQuant]):
            OfficeEnd=OfficeThresList[n]            
        elif n== len(DF[NewQuant]):
            if NewQuant in list(['UL','LL']):        
                OfficeEnd=0
            elif NewQuant in list(['UR','LR']):
                OfficeEnd=HoriPoint        
    return(OfficeEnd)

def CountData(TopRow,Box,Posi):
    print(Posi)
    if Posi not in list(['主事','技師','雇']):
        #Get Top Column
        BoxCand=[d for d in TopRow if (len(d['description'])==1) or(len(d['description'])==2)][0]
        BoxWidth=max(BoxCand['bounding_poly'][2].x-BoxCand['bounding_poly'][0].x,
                     BoxCand['bounding_poly'][1].x-BoxCand['bounding_poly'][0].x)
        
        Thres=BoxWidth/10
        res, last = [[]], None
        for x in TopRow:
            if last is None or abs(last['bounding_poly'][1].x - x['bounding_poly'][1].x) <= Thres:
                res[-1].append(x)
            else:
                res.append([x])
            last = x
            
            Edges=[d[0]['bounding_poly'][1].x for d in res]
            
            #Get Row
            BoxCand=[d for d in TopRow if len(d['description'])==1or(len(d['description'])==2)][0]
            BoxHeight=max(BoxCand['bounding_poly'][2].y-BoxCand['bounding_poly'][0].y,
                         BoxCand['bounding_poly'][1].y-BoxCand['bounding_poly'][0].y)
            
            RowList=[]
            BoxCols=[d for d in Box if d['bounding_poly'][1].x>Edges[0]*0.95]
            
            TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
            BtmHeight=TopHeight+BoxHeight*2
            RowList.append(TopHeight)
            
            #TopRow
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            while len(ConflictBox)>0:
                BtmHeight=int(BtmHeight+BoxHeight*0.5)
                ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
                if BtmHeight==TopHeight+BoxHeight*10:
                    break
            
            #Second Row
            BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
            TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
            BtmHeight=TopHeight+BoxHeight*2
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            while len(ConflictBox)>0:
                BtmHeight=BtmHeight+BoxHeight*0.5
                ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
                if BtmHeight==TopHeight+BoxHeight*10:
                    break
            RowList.append(TopHeight)
            
            #Third Row
            BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
            TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
            BtmHeight=TopHeight+BoxHeight*3
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            while len(ConflictBox)>0:
                BtmHeight=BtmHeight+BoxHeight*0.5
                ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
                if BtmHeight==TopHeight+BoxHeight*10:
                    break
            RowList.append(TopHeight)
            
            #Fourth Row
            BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
            TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
            BtmHeight=TopHeight+BoxHeight*4
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            while len(ConflictBox)>0:
                BtmHeight=BtmHeight+BoxHeight*0.5
                ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
                if BtmHeight==TopHeight+BoxHeight*10:
                    break
            RowList.append(TopHeight)
    
        Data={}
        for n in range(len(Edges)):
            Data[str(n)]=[]

        import numpy as np
        for element in Box:
            MinDist=min([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])
            Index=np.where(np.array([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])==MinDist)[0][0]
            Data[str(Index)].append(element)

        for col in list(Data.keys()):
            RowData={'Wage1':[],'Name1':[],'Wage2':[],'Name2':[]}
            for word in Data[col]:
                if RowList[0]<word['Center']['YCenter']<RowList[1]:
                    RowData['Wage1'].append(word)
                if RowList[1]<word['Center']['YCenter']<RowList[2]:
                    RowData['Name1'].append(word)
                if RowList[2]<word['Center']['YCenter']<RowList[3]:
                    RowData['Wage2'].append(word)
                if RowList[3]<word['Center']['YCenter']:
                    RowData['Name2'].append(word)
            Data[col]=RowData
        return(Data)

    if Posi == '雇':
        #Get Top Column
        BoxCand=[d for d in TopRow if len(d['description'])==1][0]
        BoxWidth=max(BoxCand['bounding_poly'][2].x-BoxCand['bounding_poly'][0].x,
                     BoxCand['bounding_poly'][1].x-BoxCand['bounding_poly'][0].x)
        
        Thres=BoxWidth/10
        res, last = [[]], None
        for x in TopRow:
            if last is None or abs(last['bounding_poly'][1].x - x['bounding_poly'][1].x) <= Thres:
                res[-1].append(x)
            else:
                res.append([x])
            last = x
        
        Edges=[d[0]['bounding_poly'][1].x for d in res]
        
        #Get Row
        BoxCand=[d for d in TopRow if len(d['description'])==1][0]
        BoxHeight=max(BoxCand['bounding_poly'][2].y-BoxCand['bounding_poly'][0].y,
                     BoxCand['bounding_poly'][1].y-BoxCand['bounding_poly'][0].y)
        
        RowList=[]
        BoxCols=[d for d in Box if d['bounding_poly'][1].x>Edges[0]*0.95]
        
        TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
        BtmHeight=TopHeight+BoxHeight*8
        RowList.append(TopHeight)
        
        #TopRow
        ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
        while len(ConflictBox)>1:
            BtmHeight=BtmHeight+BoxHeight*0.5
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            if BtmHeight==TopHeight+BoxHeight*2:
                break
        
        #Second Row
        BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
        TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
        BtmHeight=TopHeight+BoxHeight*5
        ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
        
        while len(ConflictBox)>1:
            BtmHeight=BtmHeight+BoxHeight*0.5
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            if BtmHeight==TopHeight+BoxHeight:
                break
        
        #Third Row
        BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
        TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
        BtmHeight=TopHeight+BoxHeight*8
        ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
        while len(ConflictBox)>0:
            BtmHeight=BtmHeight+BoxHeight*0.5
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            if BtmHeight==TopHeight+BoxHeight*2:
                break
        RowList.append(TopHeight)
        
                
        #infer Columns from BtmRows
        BtmRow=[d for d in Box if RowList[1]<=d['bounding_poly'][0].y]
        res, last = [[]], None
        for x in BtmRow:
            if last is None or abs(last['bounding_poly'][1].x - x['bounding_poly'][1].x) <= Thres:
                res[-1].append(x)
            else:
                res.append([x])
            last = x
        
        BtmEdges=[d[0]['bounding_poly'][1].x for d in res]

        if len(Edges)>len(BtmEdges):
            Edges=Edges
        else:
            Edges=BtmEdges
        Data={}
        for n in range(len(Edges)):
            Data[str(n)]=[]

        import numpy as np
        for element in Box:
            MinDist=min([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])
            Index=np.where(np.array([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])==MinDist)[0][0]
            Data[str(Index)].append(element)

        for col in list(Data.keys()):
            RowData={'Name1':[],'Name2':[],'Name3':[],}
            for word in Data[col]:
                if word['Center']['YCenter']<RowList[0]:
                    RowData['Name1'].append(word)
                if RowList[0]<word['Center']['YCenter']<RowList[1]:
                    RowData['Name2'].append(word)
                if RowList[1]<word['Center']['YCenter']:
                    RowData['Name3'].append(word)
            Data[col]=RowData
        return(Data)
        
    if Posi in list(['主事','技師']):
        #infer Columns from TopRows
        BoxCand=[d for d in TopRow if len(d['description'])==1 or(len(d['description'])==2)][0]
        BoxWidth=max(BoxCand['bounding_poly'][2].x-BoxCand['bounding_poly'][0].x,
                     BoxCand['bounding_poly'][1].x-BoxCand['bounding_poly'][0].x)
        Thres=BoxWidth/10
        res, last = [[]], None
        for x in TopRow:
            if last is None or abs(last['bounding_poly'][1].x - x['bounding_poly'][1].x) <= Thres:
                res[-1].append(x)
            else:
                res.append([x])
            last = x
        
        Edges=[d[0]['bounding_poly'][1].x for d in res]

        #Row Detection
        BoxCand=[d for d in TopRow if len(d['description'])==1 or(len(d['description'])==2)][0]
        BoxHeight=max(BoxCand['bounding_poly'][2].y-BoxCand['bounding_poly'][0].y,
                     BoxCand['bounding_poly'][1].y-BoxCand['bounding_poly'][0].y)
        
        RowList=[]

        #TopRow
        BoxCols=[d for d in Box if d['bounding_poly'][1].x>Edges[0]*0.95]
        TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
        BtmHeight=TopHeight+BoxHeight*4
        RowList.append(TopHeight)
        
        ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
        while len(ConflictBox)>0:
            BtmHeight=BtmHeight+BoxHeight*0.5
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            if BtmHeight==TopHeight+BoxHeight*10:
                break
        
        #Second Row
        BoxCols=[d for d in Box if d['bounding_poly'][0].y>BtmHeight]
        TopHeight=min([d['bounding_poly'][0].y for d in BoxCols ])
        BtmHeight=TopHeight+BoxHeight*15
        ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
        while len(ConflictBox)>0:
            BtmHeight=BtmHeight+BoxHeight*0.5
            ConflictBox= [d for d in BoxCols if d['bounding_poly'][0].y<=BtmHeight<=d['bounding_poly'][2].y]
            if BtmHeight==TopHeight+BoxHeight*2:
                break
        RowList.append(TopHeight)
        
        #infer Columns from BtmRows
        BtmRow=[d for d in Box if RowList[1]<=d['bounding_poly'][0].y]
        res, last = [[]], None
        for x in BtmRow:
            if last is None or abs(last['bounding_poly'][1].x - x['bounding_poly'][1].x) <= Thres:
                res[-1].append(x)
            else:
                res.append([x])
            last = x
        
        BtmEdges=[d[0]['bounding_poly'][1].x for d in res]

        if len(Edges)>len(BtmEdges):
            Edges=Edges
        else:
            Edges=BtmEdges

        import numpy as np
        Data={}
        for n in range(len(Edges)):
            Data[str(n)]=[]
        
        for element in Box:
            MinDist=min([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])
            Index=np.where(np.array([abs(Edge-element['bounding_poly'][1].x) for Edge in Edges])==MinDist)[0][0]
            Data[str(Index)].append(element)
        
        for col in list(Data.keys()):
            RowData={'Wage1':[],'Name1':[]}
            for word in Data[col]:
                if RowList[0]<word['Center']['YCenter']<RowList[1]:
                    RowData['Wage1'].append(word)
                if RowList[1]<word['Center']['YCenter']:
                    RowData['Name1'].append(word)
            Data[col]=RowData
        return(Data)

def CountDataNDL(Index,OfficeEnd,FinalQuadrantPosi,HoriPoint,VertPoint,RightX,LeftX,origin,Year,Page,NewQuant):
    f = open(origin+'Tokyo_Jobs/Processed_Data/'+str(Year)+'/NDL/'+'Page{:03d}'.format(Page)+'.json', encoding="utf8")
     
    # returns JSON object as
    # a dictionary
    data = json.load(f)[0]
    NDLData=[]
    for d in data:
        NewNDLDict={}
        NewNDLDict['Center']=[int((d[0]+d[2])/2),int((d[1]+d[3])/2)]
        NewNDLDict['inferText']=d[4]
        NDLData.append(NewNDLDict)
    
    if Index<len(FinalQuadrantPosi)-1:
        if NewQuant=='UR':
            NDFBox=[d for d in NDLData if (HoriPoint<=d['Center'][0]<=3000)&(0<=d['Center'][1]<=VertPoint)]
        if NewQuant=='LR':
            NDFBox=[d for d in NDLData if (HoriPoint<=d['Center'][0]<=3000)&(VertPoint<=d['Center'][1]<=3000)]
        if NewQuant=='UL':
            NDFBox=[d for d in NDLData if (0<=d['Center'][0]<=HoriPoint)&(0<=d['Center'][1]<=VertPoint)]
        if NewQuant=='LL':
            NDFBox=[d for d in NDLData if (0<=d['Center'][0]<=HoriPoint)&(VertPoint<=d['Center'][1]<=3000)]
        
        WordNDFBox=[d['inferText'] for d in NDFBox if LeftX<=d['Center'][0]<=RightX]
        return(WordNDFBox)
    
    if Index==len(FinalQuadrantPosi)-1:
        if NewQuant=='UR':
            NDFBox=[d for d in NDLData if (HoriPoint<=d['Center'][0]<=3000)&(0<=d['Center'][1]<=VertPoint)]
        if NewQuant=='LR':
            NDFBox=[d for d in NDLData if (HoriPoint<=d['Center'][0]<=3000)&(VertPoint<=d['Center'][1]<=3000)]
        if NewQuant=='UL':
            NDFBox=[d for d in NDLData if (0<=d['Center'][0]<=HoriPoint)&(0<=d['Center'][1]<=VertPoint)]
        if NewQuant=='LL':
            NDFBox=[d for d in NDLData if (0<=d['Center'][0]<=HoriPoint)&(VertPoint<=d['Center'][1]<=3000)]
        
        WordNDFBox=[d['inferText'] for d in NDFBox if OfficeEnd<=d['Center'][0]<=RightX]
        return(WordNDFBox)