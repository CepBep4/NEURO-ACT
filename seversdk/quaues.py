import json
import datetime

class Quaues:
    def __init__(self):
        """
        **Quaues** - класс для работы с очередями задач.
        Этот класс предоставляет методы для управления очередями задач, включая добавление задач, получение следующей задачи и управление очередями ожидания.
        
        **Логика работы**
        1. Проверяем обычную очередь задач.
        2. Если очередь пуста, проверяем очередь ожидания.
        
        **Структура очереди**
        baseQueue - [
            {track_id: str, handled: bool, error: bool ...},
            ...
        ]
        pendingQueue - [
            {track_id: str, handled: bool, error: bool ...},
            ...
        ]
        """
        
        #Распаршиваем jsonl для базовой очереди
        self.baseQueue = []
        with open("quaues/ai_queue.jsonl", "r") as file:
            for line in file:
                self.baseQueue.append(json.loads(line.strip()))
        
        #Распаршиваем jsonl для базовой очереди
        self.pendingQueue = []
        with open("quaues/pending_queue.jsonl", "r") as file:
            for line in file:
                self.pendingQueue.append(json.loads(line.strip()))
    
    #Выдаём следущие данные из очереди
    def getNextTask(self):
        for iteration, task in enumerate(self.baseQueue):
            if not task["handled"] and not task["error"]:
                self.baseQueue[iteration]["handled"] = True  #Отмечаем задачу как обработанную
                
                #Сохраняем изменения в файле
                with open("quaues/ai_queue.jsonl", "w") as file:
                    for item in self.baseQueue:
                        file.write(json.dumps(item) + "\n")
                
                return task["_taskData"]  #Возвращаем данные задачи
            
        #Выдаём следующую задачу из очереди ожидания
        for iteration, task in enumerate(self.pendingQueue):
            if not task["handled"] and task["error"]:
                self.pendingQueue[iteration]["handled"] = True
                self.pendingQueue[iteration]["error"] = False
                
                #Сохраняем изменения в файле
                with open("quaues/pending_queue.jsonl", "w") as file:
                    for item in self.baseQueue:
                        file.write(json.dumps(item) + "\n")
                
                return task["_taskData"]
        
        return None #Если нет задач в очереди
           
    #Добавляем задачу в очередь ожидания 
    def setErrorTask(self, task: dict) -> None:
        for iteration, item in enumerate(self.baseQueue):
            if item["track_id"] == task["track_id"]:
                self.baseQueue[iteration]["error"] = True
                self.baseQueue[iteration]["handled"] = False  # Отмечаем задачу как не обработанную
                self.pendingQueue.append(self.baseQueue[iteration]) if not self._findTaskByTrackIdInPendingQuaue(self.baseQueue[iteration]["track_id"]) else None # Добавляем в очередь ожидания

                #Сохраняем изменения в файле
                with open("quaues/pending_queue.jsonl", "w") as file:
                    for item in self.pendingQueue:
                        file.write(json.dumps(item) + "\n")
            
    #Добавлем задачу в очередь
    def addTaskToQueue(self, task: dict):
        
        taskStructure = {
            "track_id": task["track_id"],  # Уникальный идентификатор задачи
            "handled": False,  # Задача не обработана
            "error": False, # Задача не имеет ошибок
            "_taskData": task #Сохраняем данные для задачи
            # "time_last_handle":datetime.datetime.now() #Время попадения в очередь
        }
        
        with open("quaues/ai_queue.jsonl", "a") as file:
            file.write(json.dumps(taskStructure) + "\n")
        self.baseQueue.append(taskStructure)
        
    #Поиск задачи по track_id
    def _findTaskByTrackIdInPendingQuaue(self, track_id: str):            
        for task in self.pendingQueue:
            if task["track_id"] == track_id:
                return True
        return False  # Если задача не найдена
    
if __name__ == "__main__":
    #Тестирование модуля Quaues
    q = Quaues()
    
    task = {
        "text": "Привет друзья, как дела?",
        "track_id": f"DC-00001_CAL-a1b2c3d4",
        "time_stamp": "99.99.9999 99:99:99",
        "file_handled": "audo.mp3"
    }
    
    q.addTaskToQueue(task)
    task = q.getNextTask()
    q.setErrorTask(task)