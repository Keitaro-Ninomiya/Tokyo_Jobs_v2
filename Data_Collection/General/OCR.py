import requests, uuid, time,json,base64
import json, os, cv2,pandas as pd

def Clova(origin,Page,api_url,secret_key):    
    file_path=origin+'Tokyo_Jobs/Raw_Data/Metropolitan_DA/1942/HQ/Page'+'{:03d}'.format(Page)+'.jpg'
    with open(file_path,'rb') as f:
        file_data = f.read()
    request_json = {
                'images': [
                    {
                        'format': 'jpg',
                        'name': 'demo',
                        'data':base64.b64encode(file_data).decode()}],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time() * 1000)),
                'lang':'ja'
                }
    payload = json.dumps(request_json).encode("UTF-8")
    headers = {'X-OCR-SECRET': secret_key,
              'Content-Type': 'application/json'}
    response = requests.request("POST", api_url, headers=headers, data = payload)
    Json=json.loads(response.text)['images'][0]
    return(Json['fields'])