# IoT-Project : PiFinder
## 專案動機  
有時候會找不到東西在哪裡，自己找有時候又會找很久，因此想做一個可以幫人找物品的工具，節省找東西的時間。

## Component
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
>$ python3 main.py
>```
>![image](https://user-images.githubusercontent.com/86181854/148670887-4f8b9a1c-25a8-481c-ae4b-7b543b32085f.png)  

>Webhook URL改成上面Forwarding 的URL再加上/callback
![image](https://user-images.githubusercontent.com/86181854/148670917-d3df5cdc-44a4-4d29-85aa-e5bbbde828a0.png)
顯示success就連接成功啦
## 步驟三:測試鏡頭

### 電路圖
![driver_and_motor](https://user-images.githubusercontent.com/86181854/148636297-a92a598e-bdae-4780-8f80-d985960a8f1f.jpg)

## Reference
http://hophd.com/raspberry-pi-stepper-motor-control/  
https://s761111.gitbook.io/raspi-sensor/feng-qi  
https://www.796t.com/article.php?id=45833

