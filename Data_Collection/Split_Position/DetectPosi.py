from OrganizePosi import Filter
import itertools
def DetectPosi(BoxList,OfficeThres,PosiDict,Positions,Filter='Off'):
    """
    Detects positions from a box of text items.
    """
    #In case no offices start within the box/quadrant.
    if len(OfficeThres)==0:
        Box,Office=BoxList[0][0],list(PosiDict.keys())[-1]
        #Split into Positions
        PosiList=[]

        for Posi in Positions:
            ##Detect Position Location
            NewBox=RefineBox(Box,Posi)
            LocList=[d for d in NewBox if Posi in d['description']]
            if len(LocList)>0:        
                LocX=[d for d in LocList if Posi in d['description']][0]['bounding_poly'].vertices[0].x
                LocY=[d for d in LocList if Posi in d['description']][0]['bounding_poly'].vertices[0].y
                PosiList.append({'Position':Posi,'Location':list([LocX,LocY])})
                        
        if Filter=='On':            
            #Clean Position List
            PosiList=Filter(PosiList)
            
        #Add data to DataFrame
        PosiDict[Office].append(PosiList)
        return(PosiDict)
    
    #Office Starts in Quadrant
    else:
        for n in range(len(BoxList)+1):
            if n==0:
                Box,Office=BoxList[0][n],list(PosiDict.keys())[-1]
            if n>0:
                try:
                    Box,Office=BoxList[0][n],OfficeThres[n-1]['Office']
                except:
                    continue
            
            if Office not in list(PosiDict.keys()):
                PosiDict[Office]=[]
                
            #Split into Positions
            PosiList=[]

            for Posi in Positions:
                NowBox=RefineBox(Box,Posi)

                ##Detect Position Location
                LocList=[d for d in NowBox if Posi in d['description']]
                if len(LocList)>0:        
                    LocX=[d for d in LocList if Posi in d['description']][0]['bounding_poly'].vertices[0].x
                    LocY=[d for d in LocList if Posi in d['description']][0]['bounding_poly'].vertices[0].y
                    PosiList.append({'Position':Posi,'Location':list([LocX,LocY])})

                        
            if Filter=='On':            
                #Clean Position List
                PosiList=Filter(PosiList)
                
            #Add data to DataFrame
            PosiDict[Office].append(PosiList)
        return(PosiDict)

def DetectPosiClova(BoxListCLOVA,OfficeThres,PosiDict,Positions,Filter="Off"):
    """
    Detects positions from a box of text items.
    """
    #In case no offices start within the box/quadrant.
    if len(OfficeThres)==0:
        Box,Office=BoxListCLOVA[0][0],list(PosiDict.keys())[-1]
        #Split into Positions
        PosiList=[]

        for Posi in Positions:
            ##Detect Position Location
            NewBox=RefineBoxCLOVA(Box,Posi)
            LocList=[d for d in NewBox if Posi in d['inferText']]
            if len(LocList)>0:        
                LocX=int([d for d in LocList if Posi in d['inferText']][0]['boundingPoly']['vertices'][0]['x'])
                LocY=int([d for d in LocList if Posi in d['inferText']][0]['boundingPoly']['vertices'][0]['y'])
                PosiList.append({'Position':Posi,'Location':list([LocX,LocY])})
                        
        if Filter=='On':            
            #Clean Position List
            PosiList=Filter(PosiList)
            
        #Add data to DataFrame
        if PosiList!=[]:
            PosiDict[Office].append(PosiList)
        return(PosiDict)
    
    #Office Starts in Quadrant
    else:
        for n in range(len(BoxListCLOVA)+1):
            if n==0:
                Box,Office=BoxListCLOVA[0][n],list(PosiDict.keys())[-1]
            if n>0:
                try:
                    Box,Office=BoxListCLOVA[0][n],OfficeThres[n-1]['Office']
                except:
                    continue
            
            if Office not in list(PosiDict.keys()):
                PosiDict[Office]=[]
                
            #Split into Positions
            PosiList=[]

            for Posi in Positions:
                NowBox=RefineBoxCLOVA(Box,Posi)

                ##Detect Position Location
                LocList=[d for d in NowBox if Posi in d['inferText']]
                if len(LocList)>0:        
                    LocX=int([d for d in LocList if Posi in d['inferText']][0]['boundingPoly']['vertices'][0]['x'])
                    LocY=int([d for d in LocList if Posi in d['inferText']][0]['boundingPoly']['vertices'][0]['y'])
                    PosiList.append({'Position':Posi,'Location':list([LocX,LocY])})
                        
            if Filter=='On':            
                #Clean Position List
                PosiList=Filter(PosiList)

            
            #Add data to DataFrame
            PosiDict[Office].append(PosiList)
        return(PosiDict)
    


def RefineBox(Box,Position):
    '''
    Converts Google Vision output into a dictinary of items with strings with same length as position.
    '''
    Length=len(Position)
    Box=ConvertDict(Box)
    for n,text in zip(range(len(Box)),Box):
        i=1
        while (len(text['description'])<Length)and(n+i<len(Box)):
            Box[n]['description']=Box[n]['description']+Box[n+i]['description']
            i=i+1
    return(Box)     

def RefineBoxCLOVA(Box,Position):
    '''
    Converts CLOVA output into a dictinary of items with strings with same length as position.
    '''
    Length=len(Position)
    for n,text in zip(range(len(Box)),Box):
        i=1
        while (len(text['inferText'])<Length)and(n+i<len(Box)):
            Box[n]['inferText']=Box[n]['inferText']+Box[n+i]['inferText']
            i=i+1
    return(Box)     


def ConvertDict(texts):
    Dict=[]
    for n in range(len(texts)):
        try:            
            Box=texts[n]
            NewDict={}
            NewDict['description']=Box.description
            NewDict['bounding_poly']=Box.bounding_poly
            NewDict['bounding_poly']=Box.bounding_poly
            NewDict['Index']=n
            Dict.append(NewDict)
        except:
            continue
    return(Dict)


def AggregatePosi(PosiDict,PosiDict_CLOVA):  
    OfficeList=list(PosiDict.keys())
    for Office in OfficeList:
        PosiList=list(itertools.chain(*PosiDict[Office]))
        PosiListClova=list(itertools.chain(*PosiDict_CLOVA[Office]))

        AdditionList=[d for d in PosiListClova if d['Position'] not in [d['Position'] for d in list(itertools.chain(*PosiDict[Office]))]]
        if len(AdditionList)>0:
            PosiDict[Office].append(AdditionList)
    return(PosiDict)