def DetectOffice(Box, Office,VertPoint,Circle='Off'):    
    '''
    Returns a dictionary of offices and its locations in a page.
    
    Turn circle=='On' when using circle as detection sign.
    '''
    List=[]
    if Circle=='On':
        if '○' in [d['description'] for d in Box]:
            CandidateIndexList=[d['Index'] for d in Box[1:] if '○' in d['description']]
            for Index in CandidateIndexList:
                Words=''.join([d['description'] for d in Box[Index+1:Index+len(Office)]])
                CommonWords=list(set(Words)&set(Office))
                if len(CommonWords)>0:
                    List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})

        if '〇' in [d['description'] for d in Box]:
            CandidateIndexList=[d['Index'] for d in Box[1:] if '〇' in d['description']]
            for Index in CandidateIndexList:
                Words=''.join([d['description'] for d in Box[Index+1:Index+len(Office)]])
                CommonWords=list(set(Words)&set(Office))
                if len(CommonWords)>0:
                    List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})
    
    if Office[0] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[0] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})
    
    if Office[1] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[1] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})

                
    if Office[0:2] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[0:2] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})

    if Office[0:3] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[0:3] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})
                
    if Office[0:4] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[0:4] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})

    if Office[0:5] in [d['description'] for d in Box]:
        CandidateIndexList=[d['Index'] for d in Box[1:] if Office[0:5] in d['description']]
        for Index in CandidateIndexList:
            Words=''.join([d['description'] for d in Box[Index:Index+len(Office)]])
            CommonWords=list(set(Words)&set(Office))
            if len(CommonWords)>0:
                List.append({'CommonWord':CommonWords,'WordCount':len(CommonWords),'Words':Words,'Box':Box[Index]})
                
    if len(List)==0:
        return(None)
    else:        
        MaxCount=max([d['WordCount'] for d in List])
        Dict=[d for d in List if d['WordCount']==MaxCount]
        if len(Dict)==1:
            Dict=Dict[0]
            Dict['OfficeName']=Office
            return(Dict)
        if len(Dict)>1:
            TopDict=[d for d in Dict if (d['Box']['bounding_poly'].vertices[0].y<=VertPoint-50)]
            BtmDict=[d for d in Dict if (VertPoint<=d['Box']['bounding_poly'].vertices[0].y)]
            BtmDict=[d for d in BtmDict if (d['Box']['bounding_poly'].vertices[0].y<=VertPoint+250)]
            FinDict=TopDict+BtmDict
            if len(FinDict)>=1:
                Dict=FinDict[0]
            if len(FinDict)==0:
                Dict=Dict[0]
            Dict['OfficeName']=Office
            return(Dict)
