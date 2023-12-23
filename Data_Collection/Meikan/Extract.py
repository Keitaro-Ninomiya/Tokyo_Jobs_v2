from google.cloud.vision_v1 import types
import cv2

def Vision(crop,lang,client):
    success,encoded_image = cv2.imencode('.jpg', crop)
    content2 = encoded_image.tobytes()
    image_cv2 = types.Image(content=content2)
    response =  client.text_detection(image=image_cv2,
                                     image_context={"language_hints": [lang]})
    texts = response.text_annotations
    return(texts)