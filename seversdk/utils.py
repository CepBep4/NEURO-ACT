import pandas as pd


def vaildData(data):
    #Проверка данных
    needData = [
        "session_id",
        "text",
        "time_stamp",
        "file_handled"
    ]
    
    {'text': 'Привет друзья, как дела', 'session_id': 'DC-000000_CAL-a1b2c3d4', 'time_stamp': '99.99.9999 99:99:99', 'file_handled': 'audo.mp3'}
    
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