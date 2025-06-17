import json
from handler import Quaues
import yaml

class Metrics:
    def __init__(self):
        self.threadCountMax = getMaxThread()
        self.threadConut = 0
        self.queue = Quaues()
        self.version = getVersion()
        self.port = getPort()
        self.pathRecieve = "storage/received_data/"
        self.yamlConfing = loadYaml()

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

#Загрузка yaml конфигурации
def loadYaml():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)