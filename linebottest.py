#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as gpio
from picamera import PiCamera
import cv2
import numpy as np
# Use BCM GPIO references
# instead of physical pin numbers
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False) 
# Define GPIO signals to use
# Physical pins 8,10,12,16
# GPIO17,GPIO22,GPIO23,GPIO24
pin = [8,10,12,16]
piano = list([261, 293, 329, 349, 391, 440, 493, 523])
for i in range(4):
    gpio.setup(pin[i], gpio.OUT)
gpio.setup(7,gpio.OUT);
forward_sq = ['0011', '1001', '1100', '0110']
reverse_sq = ['0110', '1100', '1001', '0011']

#camera = PiCamera()
def forward(steps, delay):
    for i in range(steps):
        for step in forward_sq:
            set_motor(step)
            time.sleep(delay)
 
def reverse(steps, delay):
    for i in range(steps):
        for step in reverse_sq:
            set_motor(step)
            time.sleep(delay)
 
def set_motor(step):
    for i in range(4):
        gpio.output(pin[i], step[i] == '1')
        
def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        gpio.output(7, gpio.HIGH)
        time.sleep(half_pitch)
        gpio.output(7, gpio.LOW)
        time.sleep(half_pitch)
 
    



from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('lSo4SpwhEVgEl0cqaOuUnKPNQczgI/NuVf70rk2eOmM8sCcC92WQMroBo2aBvEjbHCiEK9J3IBKlfyjEsz/KVx2CwBB8tXtEDwGT93B/Xp0qeTynjBcn2uevEpqQjD6T1wcA2w0/+Bip0YYCU5ogPwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c45adaf072da2f196772e02c6381e232')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    gpio.setmode(gpio.BOARD)
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    
    set_motor('0000')
    '''
    #settings.py
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,'static')
    ]
    
    #urls.py
    #import static
    from django.conf.urls.static import static
    from django.conf import settings
    
    #加入這一行
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    '''
    if(message=="phone"):
        lookfor(message)
        line_bot_api.reply_message(reply_token, TextSendMessage(text = "find"))
        
        
        #for p in piano:
        #    play(p, 1)
        #time.sleep(2)
        #camera.capture('tcc.jpg')
    elif(message=="bottle"):
        lookfor(message)
        #if(true):
        line_bot_api.reply_message(reply_token,ImageSendMessage(
        original_content_url='https://github.com/Hanky2000/IoT-Project/blob/main/melon.jpg',
        preview_image_url='https://github.com/Hanky2000/IoT-Project/blob/main/melon.jpg'
        ))
        reverse(360,0.01)
        #else:    
        
    else:                
        line_bot_api.reply_message(reply_token, TextSendMessage(text = "物件未登錄"))
def lookfor(string):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())    
    # open webcam video stream
    cap = cv2.VideoCapture(0)    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    sequences = [0, 1, 2, 3, 4, 5]
    for i in sequences:
        forward(60, 0.01)
        time.sleep(5)        
        
            
    # When everything done, release the capture
    cap.release()

    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

gpio.cleanup()

