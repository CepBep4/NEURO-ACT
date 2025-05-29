#Проверка настройки сервера
import requests
import json

def testServer():
    #Тестовые данные
    url = "http://127.0.0.1:8000/sendHandle/"
    
    file_path = "testdata/test.mp3"
    
    data = {
        "text": "Привет друзья, как дела",
        "session_id": "DC-000000_CAL-a1b2c3d4",
        "time_stamp": "99.99.9999 99:99:99",
        "file_handled": "audo.mp3"
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path, file, 'application/octet-stream')
        }
        data = {
            'json_data': json.dumps(data)
        }

        response = requests.post(url, files=files, data=data)

    return response.status_code, response.text

print(testServer())
    