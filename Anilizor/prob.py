import requests

FASTAPI_URL = "http://localhost:8000/get_doc"  # Используйте правильный URL

def fastapi():
    response = requests.get(FASTAPI_URL)
    if response.status_code == 200:
        result = response.json()
        print(f"Ответ от FastAPI: {result}")
        return result
    else:
        print(f"Ошибка: {response.status_code}")
        return {"error": response.text}

# Пример использования
result = fastapi()
print(result)
