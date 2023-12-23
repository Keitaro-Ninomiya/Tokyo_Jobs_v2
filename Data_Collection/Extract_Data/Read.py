import os
import numpy as np
import cv2
import re
from google.cloud.vision_v1 import types
import pandas as pd

def Download(filepath,Dept,Office,Posi,Page):
    path=os.path.join(filepath,Dept,Office,Posi,'Image'+str(Page)+'.png')
    stream = open(path, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
    return(image)

def Vision(crop,lang,client):
    success,encoded_image = cv2.imencode('.jpg', crop)
    content2 = encoded_image.tobytes()
    image_cv2 = types.Image(content=content2)
    response =  client.text_detection(image=image_cv2,
                                     image_context={"language_hints": [lang]})
    texts = response.text_annotations
    return(texts)

def PosiLetter(Posi):
    df=pd.read_csv("C:\\Users\\Keitaro Ninomiya\\Box\\Research Notes (keitaro2@illinois.edu)\\Tokyo_Jobs\\Processed_Data\\PositionCrosswalk.csv")
    Row=df[df['Data']==Posi]['FirstLetter']
    Kanji=Row.to_string()[5::]
    if len(Kanji)>1:
        Kanji=Row.to_string()[5::].split(",")
    return(Kanji)

def Template(Box):
    ymax,ymin=max([d.y for d in Box[0].vertices]),min([d.y for d in Box[0].vertices])
    xmax,xmin=max([d.x for d in Box[0].vertices]),min([d.x for d in Box[0].vertices])
    Height,Width=(ymax-ymin),(xmax-xmin)

    if Width>1.5*Height:
        PosiName='True'
    if Width<=1.5*Height:
        PosiName='False'
    return(PosiName)

def Crop(image,client,Posi,Part,Page):
    if Part==2:
        return(Crop2(image,client,Posi))
    if Part==3:
        return(Crop3(image,client,Posi,Page))

def Crop2(image,client,Posi):   
    NumList=['三','四','五','上']
    HH,WW=image.shape[:2]
    crop=image[0:200,0:WW]
    
    texts=Vision(crop,'ja',client)
    Box=[d.bounding_poly  for d in texts if (d1 in d.description for d1 in PosiLetter(Posi))]
    
    #If data returns empty data frame, re-do the OCR using Chinese letters
    if len(Box)==0:
        texts=Vision(crop,'zh',client)
        Box=[d.bounding_poly  for d in texts if (d1 in d.description for d1 in PosiLetter(Posi))]
        Top=min([d.y for d in Box[0].vertices])
    if len(Box)!=0:
        Top=min([d.y for d in Box[0].vertices])
    image2=image[Top:HH,0:WW]
    
    Length=160
    TopImg=image2[0:Length,0:WW]
    
    image3=image2[Length:HH,0:WW]
    crop=image3[0:150]
    
    texts=Vision(crop,'ja',client)
    Box=[d.bounding_poly  for d in texts if (d1 in d.description for d1 in NumList)]   
    if len(Box)==0:
        texts=Vision(crop,'zh',client)
        Box=[d.bounding_poly  for d in texts if (d1 in d.description for d1 in NumList)]
        
    Top=min([d.y for d in Box[0].vertices])
    if Top>50:
        Top=0
    BtmImg=image3[Top:Length+Top,0:WW]
    return(list((TopImg,BtmImg)))

def Crop3(image,client,Posi,Page):
    if Page==1:        
        PosiName="True"
        HH,WW=image.shape[:2]
        crop=image[0:200,0:WW]
        # First Row
        texts=Vision(crop,'zh',client)
        Box=[d.bounding_poly  for d in texts[1::] if sum(d1 in d.description for d1 in PosiLetter(Posi))>=1]

        if len(Box)==0:
            texts=Vision(crop,'ja',client)
            Box=[d.bounding_poly  for d in texts[1::] if sum(d1 in d.description for d1 in PosiLetter(Posi))>=1]
            if len(Box)==0:
                Box=[d.bounding_poly  for d in texts]
                PosiName='False'
        if PosiName=='False':
            PosiName=Template(Box)
        Top=min([d.y for d in Box[0].vertices])
        if Top<0:
            Top=0
            
        if PosiName=='True':
            Length1=95
        if PosiName=='False':
            Length1=150
        TopImg=image[Top:Top+Length1,0:WW]
        image2=image[Top+Length1:HH,0:WW]
    if Page!=1:
        PosiName='NA'
        HH,WW=image.shape[:2]
        crop=image[30:200,0:WW]
        # First Row
        texts=Vision(crop,'zh',client)
        Box=[d.bounding_poly  for d in texts]
        if len(Box)==0:
            texts=Vision(crop,'ja',client)
            Box=[d.bounding_poly  for d in texts]

        Length1=100
        Top=min([d.y for d in Box[0].vertices])
        TopImg=image[Top:Top+Length1,0:WW]
        image2=image[Top+Length1:HH,0:WW]
    
    #Second Row
    texts=Vision(image2,'zh',client)
    Box=[d.bounding_poly  for d in texts]
    if len(Box)==0:
        texts=Vision(image2,'ja',client)
        Box=[d.bounding_poly  for d in texts]
    
    Top=min([d2.y for d2 in [d1[0] for d1 in [d.vertices for d in Box]]])
    if Top<0:
        Top=0
    Length2=100
    HH,WW=image2.shape[:2]
    MidImg=image2[Top:Top+Length2,0:WW]
    image3=image2[Top+Length2:HH,0:WW]
    
    #Third Row
    texts=Vision(image3,'zh',client)
    Box=[d.bounding_poly  for d in texts]
    if len(Box)==0:
        texts=Vision(image3,'ja',client)
        Box=[d.bounding_poly  for d in texts]

    if len(Box)==0:
        Top=0
    if len(Box)!=0:
        Top=min([d2.y for d2 in [d1[0] for d1 in [d.vertices for d in Box]]])
        
    if Top<0:
        Top=0
    HH,WW=image3.shape[:2]
    BtmImg=image3[Top:Top+Length2,0:WW]
    
    return(list((TopImg,MidImg,BtmImg,PosiName)))

def GetPosi(Year,dta,Dept,Office):
    if Dept not in list(dta[Year].keys()):
        Posi='NA'
        return(Posi)
    if Office not in list(dta[Year][Dept].keys()):
        Posi='NA'
        return(Posi)
    if Office in list(dta[Year][Dept].keys()):
        Posi=list(dta[Year][Dept][Office]['Positions'].keys())[-1]
        return(Posi)
    

def ExtractName(texts,FormatVar):
    if FormatVar=='Horizontal':        
        LastLetters=texts[0].description.split("\n")[-1]
        LongName=max(texts[0].description.split("\n"), key=len)
        
    if FormatVar=='Vertical':
        LastLetters=''
        NameList=texts[0].description.split("\n")
        for Name in NameList:
            LastLetter=Name[-1]
            LastLetters=LastLetters+LastLetter
        LongName=LastLetters
    return ({"LastLetters":LastLetters,"LongName":LongName})

def AccuracyCheck(texts):
    FirstLetters=texts[0].description.split("\n")[0]
    LastLetters=texts[0].description.split("\n")[-1]
    STD=np.std([len(FirstLetters),len(LastLetters)])
    return(STD)

def char_is_hiragana(c) -> bool:
    return u'\u3040' <= c <= u'\u309F'
def string_is_hiragana(s: str) -> bool:
    return all(char_is_hiragana(c) for c in s)
def is_katakana(value):
    return re.match(r'^[\u30A0-\u30FF]+$', value) is not None

def CountFemale(LastNames):
    FemaleNum=sum([(d=='子') or (d=='江') or (d=='了') or (string_is_hiragana(d)) or (is_katakana(d)) for d in LastNames])
    return(FemaleNum)

def AddData(texts):
    Val=AccuracyCheck(texts)
    FormatVar=Format(texts)
    if Val<0.5:
        Accuracy='Accurate'
    if (Val>=0.5) and (Val<1):
        Accuracy='Moderate'
    if (Val>=1):
        Accuracy='Inaccurate'
    LastNames=ExtractName(texts,FormatVar)['LastLetters']
    LongName=ExtractName(texts,FormatVar)['LongName']
    d={'Accuracy':Accuracy,'LastLetters':LastNames,'Size':len(LongName),'FemaleCount':CountFemale(LastNames)}
    return(d)

def Organize(Dict):
    Keys=list(Dict.keys())
    SizeList=[]
    FemaleList=[]
    for key in Keys:
        SizeList.append(Dict[key]['Size'])
        FemaleList.append(Dict[key]['FemaleCount'])
    Size,FemaleCount=max(SizeList),max(FemaleList)
    return({'FemaleCount':FemaleCount,'Size':Size})

def Format(texts):
    Box=texts[0].bounding_poly
    xmin,xmax=min([d.x for d in Box.vertices]),max([d.x for d in Box.vertices])
    ymin,ymax=min([d.y for d in Box.vertices]),max([d.y for d in Box.vertices])
    
    Width=xmax-xmin
    Height=ymax-ymin
    
    if Height>1.5*Width:
        FormatVar='Vertical'
    if Height<=1.5*Width:
        FormatVar='Horizontal'
    return(FormatVar)

def ExtractData(ImgList,client):
    k=len(ImgList)-1
    #Use OCR to get data from each row
    Letters=list(map(Vision,ImgList[0:3],['ja']*k,[client]*k))
    #Convert OCR result to data
    Data=list(map(AddData,Letters))
    #Aggregate into nested dictionary
    MainDict={}
    for Dict in Data:
        Index=str(Data.index(Dict))
        MainDict[Index]=Dict
    return(MainDict)

   
def Show(ImgList):
    cv2.imshow('TopImg',ImgList[0])
    cv2.imshow('MidImg',ImgList[1])
    cv2.imshow('BtmImg',ImgList[2])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
