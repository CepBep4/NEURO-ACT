import json

class Metrics:
    def __init__(self):
        self.threadCountMax = getMaxThread()
        self.threadConut = 0
        self.queue = []
        self.handledFiles = []#getHandledFiles()
        self.version = getVersion()
        self.port = getPort()
    
    def setQueue(self) -> None:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        data['queue'] = self.queue
        with open('metrics/variables.json', 'w') as f:
            json.dump(data, f)
    
    def setHandledFiles(self) -> None:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        data['handled_files'] = self.handledFiles
        with open('metrics/variables.json', 'w') as f:
            json.dump(data, f)

#Обработанные файлы
def getHandledFiles() -> list:
    with open('metrics/variables.json', 'r') as f:
        data = json.load(f)
    return data['handled_files']

#Максимальное количество потоков
def getMaxThread() -> int:
    with open('metrics/variables.json', 'r') as f:
        data = json.load(f)
    return data['thread_count_max']

#Порт
def getPort() -> int:
    with open('metrics/variables.json', 'r') as f:
        data = json.load(f)
    return data['port']

#Версия программы
def getVersion() -> str:
    with open('metrics/variables.json', 'r') as f:
        data = json.load(f)
    return data['version']

#Очередь задач
def getQueue() -> list:
    with open('metrics/variables.json', 'r') as f:
        data = json.load(f)
    return data['queue']