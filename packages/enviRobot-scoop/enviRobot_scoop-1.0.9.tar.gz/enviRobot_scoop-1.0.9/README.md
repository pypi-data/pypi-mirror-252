# eco_ask

.env檔請填入以下資訊, 並放置於你終端機的工作目錄
```
LINE_CHANNEL_TOKEN=
LINE_CHANNEL_SECRET=
OPENAI_KEY=
GOOGLE_API_KEY=Geocoding API key
IMGUR_ID=
#DEVICE_MAP_CSV_PATH=有device_id,lat,lon對應的csv位置 如果需要使用get_rawdata mode=10min的話
```
使用pip安裝
```
pip install enviRobot-scoop
```
使用scoop-handler
```
from enviRobot_scoop import enviRobot_scoop
enviRobot_scoop.handle_enviRobot(dic_params, question, websocket)
```

requirements 裡面要根據不同作業系統設定 kaleido 套件的版號
kaleido==0.2.1 <-- linux
kaleido==0.1.0post1 <-- windows