# IoT-Project : PiFinder
## 專案動機  
有時候會找不到東西在哪裡，自己找有時候又會找很久，因此想做一個可以幫人找物品的工具，節省找東西的時間。

## Component
### Hardware  

樹莓派3 *	1  
Neural Compute Stick 2 * 1  
麵包板	1  
OV2640攝影鏡頭模組 *	1  
步進馬達 *	1  
杜邦線	數條  
蜂鳴器 *	1  
筷子	1雙  
PP塑膠板(白色、5mm) *	1  
泡棉膠(24mm*5m) *	1  
保麗龍膠 * 1  

### Software  
tensorflow  
keras  
openCV

## 步驟一 : 安裝套件 : tensorflow,keras

#### (1)安裝必要的依賴項
```
$ sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran python-dev libgfortran5 \libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev \liblapack-dev cython openmpi-bin libopenmpi-dev libatlas-base-dev python3-dev  
```
#### (2)安裝相關python包
```
$ sudo pip install keras_applications==1.0.8 --no-deps  
$ sudo pip install keras_preprocessing==1.1.0 --no-deps  
$ sudo pip install h5py==2.9.0  
$ sudo pip install pybind11  
$ pip install -U --user six wheel mock
```
#### (3)在樹苺派下載
>連結:https://github.com/lhelontra/tensorflow-on-arm/releases  
我選tensorflow-2.0.0-cp37-none-linux_armv7l.whl這個套件下載

#### (4)安裝套件
```
$ cd Downloads  
$ sudo pip3 install tensorflow-2.0.0-cp37-none-linux_armv7l.whl  
$ sudo pip3 install keras
```

#### (5)確認套件是否安裝
```
$ python3  
>>>from tensorflow import keras
```
若無錯誤表示成功

## 步驟二:安裝linebot
參考以下教學:  
>https://www.learncodewithmike.com/2020/06/python-line-bot.html  
>https://ithelp.ithome.com.tw/articles/10238680  
>https://ithelp.ithome.com.tw/articles/10238857  
另外可註冊ngrok帳號讓sesstion沒有2小時限制

註冊好後輸入以下指令再連線
```
./ngrok authtoken {your authtoken}
```
```
./ngrok http 80
```
>會像這樣  
![image](https://user-images.githubusercontent.com/86181854/148670862-86301365-edfc-459a-a30b-dc38b1c194ff.png)

>再從另一個terminal執行py檔
>```
>$ sudo python3 main.py
>```
>![image](https://user-images.githubusercontent.com/86181854/148670887-4f8b9a1c-25a8-481c-ae4b-7b543b32085f.png)  

>Webhook URL改成上面Forwarding 的URL再加上/callback
![image](https://user-images.githubusercontent.com/86181854/148670917-d3df5cdc-44a4-4d29-85aa-e5bbbde828a0.png)
顯示success就連接成功啦
## 步驟三:接電路和鏡頭
### 安裝openCV  
```
$ sudo pip3 install opencv-python
```
### 電路圖
> IN1到IN4分別接Physical pins 8,10,12,16  
> +接Physical pins4，-接6Physical pins接地  
> 蜂鳴器+接Physical pins9，-接Physical pins7  
![driver_and_motor](https://user-images.githubusercontent.com/86181854/148636297-a92a598e-bdae-4780-8f80-d985960a8f1f.jpg)

## 步驟四：在teachable machine訓練模組後匯出
![image](https://user-images.githubusercontent.com/86181854/148686926-a7478c0f-0088-4b2b-8134-e4b389d6d83e.png)
>將Keras和Savedmodel兩種都下載
![image](https://user-images.githubusercontent.com/86181854/148687067-7508a7b8-8709-4974-90bb-f554063cfeb6.png)

>將圖片和keras_model.h5存在與py檔相同目錄
![2022-01-09_22h38_19](https://user-images.githubusercontent.com/86181854/148687027-6f88401b-bdef-40c2-bb15-af4c7e65c804.png)

## 步驟五：撰寫人體感測與鏡頭旋轉程式
```
#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as gpio
from picamera import PiCamera
import cv2
# Use BCM GPIO references
# instead of physical pin numbers
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False) 
# Define GPIO signals to use
# Physical pins 8,10,12,16
# GPIO14,GPIO15,GPIO18,GPIO23
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
        
    # open webcam video stream
    cap = cv2.VideoCapture(0)    
    sequences = [0, 1, 2, 3, 4, 5]
    for i in sequences:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        #gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        #boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        #boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        '''
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
        '''
        # Display the resulting frame
        cv2.imshow('frame',frame)
        forward(60, 0.01)
        time.sleep(5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
            
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
```


## 步驟六：製作硬體
運用紙板黏上泡棉膠，一邊放樹梅派和固定住的鏡頭，一邊黏著兩根竹筷，竹筷夾住步進馬達的轉軸以跟著旋轉。
## 實做照片
![63632](https://user-images.githubusercontent.com/86181854/148909013-a13ef4d5-0575-4acf-a296-4ae1dd781bf7.jpg)
## Project Demo   
https://youtu.be/nRdK89kzAxc
## Reference
http://hophd.com/raspberry-pi-stepper-motor-control/  
https://s761111.gitbook.io/raspi-sensor/feng-qi  
https://www.796t.com/article.php?id=45833  
https://github.com/weberlu88/2019-Fall-MIS-IoT-Project/blob/master/opencv_test.py?fbclid=IwAR3I-6kJx1K1zPu6S72NhBrl_9VQ1bEzyMkETBUo3KHCcHOpyZ_lHW1CnOY
