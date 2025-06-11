import threading
import multiprocessing
from worker import worker
from seversdk import loggerErrors, loggerApiReceive, loggerSystem, Metrics, vaildData
import traceback
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import shutil
import torch
import datetime

WORK_MODE = 't' # t - threadiing, p - multiprocess

#Приложение для прослушивания endpoint
app = FastAPI()

#Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#Инициализируем метрики
metrics = Metrics()

# #Иницализируем модель
# model = modelInit()

#Отдаём лог о запуске
loggerSystem.info(f'''
Программа запущена - {datetime.datetime.now()}
Макс кол-во потоков - {metrics.threadCountMax}
CUDA доступна: {torch.cuda.is_available()}
''')

#Прослушивание endpoint FAST-API
@app.post("/sendHandle/")
async def listen(file: UploadFile = File(...), json_data: str = Form(...)):
    
    #Логируем получение данных
    loggerApiReceive.info("Сервер получил новые данные")
    
    #Получаем данные
    if json_data and file:
        
        #Вытягиваем данные
        data = json.loads(json_data)
        
        #Валидация
        if not vaildData(data):
            loggerErrors.error(f"Данные не прошли валидацию")
            raise HTTPException(500, "Ошибка валидации")            
        
        #Сохраняем файл
        os.mkdir(f"storage/{data['session_id']}")
        with open(f"storage/{data['session_id']}/audio.mp3", 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        #Сохраняем json
        with open(f"storage/{data['session_id']}/metadata.json", 'w') as file:
            file.write(json.dumps(data))
    else:
        raise HTTPException(500, "Неверные данные")
    
    #Передаём в обработку
    handler(data)
        

#Менеджер по потокам, функция раздаёт задачи
def handler(data):
    #Обновляем метрики
    metrics.setHandledFiles()
    metrics.setQueue()
    
    loggerApiReceive.info(f"Данные прошли валидацию, сессия: {data['session_id']} передана в обработку")
    
    #Выдача задачи на поток
    if metrics.threadConut < metrics.threadCountMax:
        if WORK_MODE == "t":
            threading.Thread(
                target=worker,
                args=(data, metrics,)
            ).start()
        
        #Увеличиваем количество потоков в метриках
        metrics.threadConut += 1
    
    else:   
        #Добавляем в очередь
        loggerSystem.info(f"Сессия: {data['session_id']} добавлена в очередь")
        metrics.queue.append(data)