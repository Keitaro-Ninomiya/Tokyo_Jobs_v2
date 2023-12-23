def ConvertDict(texts):
    Dict=[]
    for n in range(len(texts)):
        Box=texts[n]
        NewDict={}
        NewDict['description']=Box.description
        NewDict['bounding_poly']=Box.bounding_poly
        NewDict['bounding_poly']=Box.bounding_poly
        NewDict['Index']=n
        Dict.append(NewDict)
    return(Dict)

def Filter(Page,texts,HoriPoint):
    if Page%2==0:
        Box=[d for d in texts[1:] if d.bounding_poly.vertices[0].x>HoriPoint]
    if Page%2==1:
        Box=[d for d in texts[1:] if d.bounding_poly.vertices[0].x<HoriPoint]
    return(Box)

def FilterBox(Box,List,VertPoint):
    LocationInfo=List[-1]['Box']['bounding_poly'].vertices[0]
    if LocationInfo.y<VertPoint:
        TopBox=[d for d in Box if (d['bounding_poly'].vertices[0].x<LocationInfo.x)&(d['bounding_poly'].vertices[0].y<VertPoint)]
        BtmBox=[d for d in Box if (d['bounding_poly'].vertices[0].y>VertPoint)]
        Box=TopBox+BtmBox
        for n in range(len(Box)):
            Box[n]['Index']=n
            
    if LocationInfo.y>VertPoint:
        Box=[d for d in Box if (d['bounding_poly'].vertices[0].x<LocationInfo.x)&(d['bounding_poly'].vertices[0].y>VertPoint)]
        for n in range(len(Box)):
            Box[n]['Index']=n
    return(Box)
    