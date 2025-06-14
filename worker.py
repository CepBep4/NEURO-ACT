#Импорты
from seversdk import Metrics, loggerAnalysis, loggerErrors, loggerSystem, pipe, saveToExcel
import os
import json
import traceback
import time
from seversdk import saveStructLogs

#Рекурсивня функция работающая на потоке
def worker(data: dict, metrics: Metrics):    
    #Полезная работа
    try:
        #Засекаем время
        startTime = time.time()
        
        #Получаем промпт
        with open("metrics/prompt.txt", "r") as file:
            prompt = file.read().format(text=data["text"])
        
        #Дипсиковская дистилированная модель
        response = pipe(prompt, metrics)
        
        #Формируем путь до папки results
        path = f"results/{data['track_id']}"
        
        #Создаём папку
        os.mkdir(path)
        
        #Добавляем в папку audio.mp3
        fileRequest = open(f"{metrics.pathRecieve}{data['track_id']}/audio.mp3", "rb")
        with open(f"{path}/audio.mp3", 'wb') as audio:
            audio.write(fileRequest.read())
        fileRequest.close()
        
        #Добавляем файл transript.txt
        with open(f"{path}/transcript.txt", 'w') as file:
            file.write(data['text'])
            
        #Добавляем файл ai_result.json
        with open(f"{path}/ai_result.json", 'w') as file:
            file.write(json.dumps({
                "prompt":prompt,
                "answer":response if isinstance(response, str) else response["output"]
            }))
            
        #Добавляем файл reasoning.json
        with open(f"{path}/reasoning.json", 'w') as file:
            file.write(json.dumps({
                "token_routing_map":"Временно отсутсвует" if isinstance(response, str) else response["token_routing_map"], #Карта маршрутизации токенов
                "expert_outputs":"Временно отсутсвует" if isinstance(response, str) else response["expert_outputs"], #Выводы экспертов
                "output": response if isinstance(response, str) else response["output"], #Ответ нейросети
                "logic_summary":"Временно отсутсвует" if isinstance(response, str) else response["logic_summary"], #Итоговая логика обработки
            }))
            
        #Формируем exel отчёт
        saveToExcel([{
            "№":"1", #Номер строки
            "Track ID":data["track_id"], #Айди сессии
            "Timestamp":data["time_stamp"], #Метка времени
            "Original Text":data["text"], #Текст полученный после транскрибации
            "AI Response":response if isinstance(response, str) else response["output"], #Ответ нейросети
            "Main Expert ID":"Временно отсутсвует" if isinstance(response, str) else response["expert_outputs"], #Главный эксперт
            "Routing Score":"Временно отсутсвует" if isinstance(response, str) else response["token_routing_map"], #Карта маршрутизации токенов
            "Reasoning Summary":"Временно отсутсвует" if isinstance(response, str) else response["logic_summary"], #Итоговая логика формирования ответа
        }], f"{path}/summary.xlsx")
        
        saveStructLogs(data, response, prompt) #Сохраняем структурированные логи
            
        #models-olama-deepseek-r1-deepsteel-32b ggb
        ...
        
        #Выводим лог об обработке
        loggerAnalysis.info(f"Сессия {data['track_id']} успешно обработана, время обработки: {round(time.time()-startTime, 3)}сек.")
    except Exception as e:
        traceback.print_exc()
        loggerErrors.critical(f"Данные НЕ обработаны сессия: {data['track_id']} ошибка: {e}")
        #Добавляем задачу в очередь ожидания
        metrics.queue.setErrorTask(data)
        
    #Проверяем очередь
    nextTask = metrics.queue.getNextTask()
    if nextTask:        
        #Запускаем задачу
        loggerSystem.info(f"Сессия: {nextTask['track_id']} передана в обработку")
        worker(nextTask, metrics)
    
    else:
        #Убираем поток с cчётчика
        metrics.threadConut -= 1
         
        #Завершаем работу потока
        loggerSystem.info("Поток завершил работу")
        return None