import pandas as pd
import json
import os


def vaildData(data):
    #Проверка данных
    needData = [
        "track_id",
        "text",
        "time_stamp",
        "file_handled"
    ]
    
    {'text': 'Привет друзья, как дела', 'track_id': 'DC-000000_CAL-a1b2c3d4', 'time_stamp': '99.99.9999 99:99:99', 'file_handled': 'audo.mp3'}
    
    #Проходимся по всем свойствам
    for property in needData:
        if property not in data:
            return False
    
    #Возвращаем True в случае успеха
    return True

#Сохраняет exel
def saveToExcel(data: list, save_path: str):
    columns = [
        "№",
        "Track ID",
        "Timestamp",
        "Original Text",
        "AI Response",
        "Main Expert ID",
        "Routing Score",
        "Reasoning Summary"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(save_path, index=False)
    
def saveStructLogs(data: dict, response: str | dict, prompt: str): 
        '''
            Необходимая структура `response` для правильного сохранения логов:
            ```
            if response is dict:
                response = {
                    "output": "Ответ нейросети",
                    "token_routing_map": "Карта маршрутизации токенов",
                    "expert_outputs": "Выводы экспертов",
                    "logic_summary": "Итоговая логика обработки",
                    "tokenization": "Логи токенизации (если есть)"
                }
            elif response is str:
                response = "Ответ нейросети в виде строки"
            ```
        '''
        
        path = "storage/"
        track_id = data["track_id"]
            
        #Добавляем файл ai_result.json
        with open(f"{path}ai_results/{track_id}.json", 'w') as file:
            file.write(json.dumps({
                "prompt":prompt,
                "answer":response if isinstance(response, str) else response["output"]
            }))
            
        #Добавляем файл для логов токенизации
        with open(f"{path}tokenization_logs/{track_id}.json", 'w') as file:
            file.write(json.dumps({
                "tokenization": "Временно отсутсвует" if isinstance(response, str) else response.get("tokenization", "Временно отсутсвует"), #Логи токенизации
            }))
            
        with open(f"{path}ai_results/{track_id}.json", 'w') as file:
            file.write(json.dumps({
                "prompt":prompt,
                "answer":response if isinstance(response, str) else response["output"]
            }))
        
        #Добавляем файл reasoning.json
        with open(f"{path}moe_logs/{track_id}.json", 'w') as file:
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
        }], f"{path}excel_exports/{track_id}.xlsx")