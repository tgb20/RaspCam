import cv2
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import giphypop
from requests import get
import webbrowser
from random import *


g = giphypop.Giphy()

camera = cv2.VideoCapture(0)

client = vision.ImageAnnotatorClient()

file_name = os.path.join(
    os.path.dirname(__file__),
    'image.jpg')

while True:
    return_value,image = camera.read()
    cv2.imshow('image',image)
    if cv2.waitKey(1)& 0xFF == ord('s'):
        cv2.imwrite('image.jpg',image)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            image = types.Image(content=content)
            response = client.label_detection(image=image)
            labels = response.label_annotations
            print(labels[0].description)
            results = [x for x in g.search(labels[0].description)]
            with open("response.gif", "wb") as file:
                response = get(results[randint(0, len(results))].media_url)
                file.write(response.content)
        break
camera.release()
cv2.destroyAllWindows()

f = open('result.html','w')
message = """<html>
<head></head>
<body><img style="height:100%; width:auto;" src="response.gif"></body>
</html>"""
f.write(message)
f.close()

filename = 'result.html'
webbrowser.open_new_tab('file:///Users/jacobbashista/Desktop/result.html')
