from PIL import Image
import cv2
import base64
import time
import requests
from io import BytesIO

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

time.sleep(2)

url = 'http://127.0.0.1:8000/narrate_stream'
params = {
    'user_id': 693,
    'narrator': 'Sir David Attenborough'
}

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('webcam', frame)
        # Convert the frame to a PIL image
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image
        max_size = 250
        ratio = max_size / max(pil_img.size)
        new_size = tuple([int(x*ratio) for x in pil_img.size])
        resized_img = pil_img.resize(new_size, Image.LANCZOS)

        buffered = BytesIO()
        resized_img.save(buffered, format='JPEG')
        img_str = base64.b64encode(buffered.getvalue())

        params['b64_string'] = f'data:image/jpeg;base64,{img_str.decode("utf-8")}'

        with requests.post(url, json=params, stream=True) as r:
            for chunk in r.iter_content(None, decode_unicode=True):
                if chunk:
                    print(chunk, end='', flush=True)

        cv2.waitKey(0)
