import requests
import os

def main():
    print("Инициализация протокола сбора данных...\n")

    # ==========================================
    # ЭТАП 1: РАЗВЕДКА
    # ==========================================
    print("=== ЭТАП 1: РАЗВЕДКА ===")
    target_name = input("Введите имя цели (например, michael или anna): ").strip().lower()
    
    try:
        # Запросы к открытым API
        age_response = requests.get(f"https://api.agify.io?name={target_name}")
        gender_response = requests.get(f"https://api.genderize.io?name={target_name}")
        
        # Проверка на успешность запроса
        age_response.raise_for_status()
        gender_response.raise_for_status()
        
        age_data = age_response.json()
        gender_data = gender_response.json()
        
        age = age_data.get("age", "неизвестен")
        gender = gender_data.get("gender", "неизвестен")
        probability = gender_data.get("probability", 0) * 100
        
        gender_str = "женского" if gender == "female" else "мужского"
        print(f"Цель: {target_name.capitalize()}. Вероятный возраст: {age}. Вероятность {gender_str} пола: {probability:.1f}%.\n")
        
    except requests.exceptions.RequestException as e:
        print(f"[!]Ошибка на этапе разведки: {e}\n")
        return

    # ==========================================
    # ЭТАП 2: МАСКИРОВКА
    # ==========================================
    print("=== ЭТАП 2: МАСКИРОВКА ===")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) СекретныйАгентБот/1.0",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    params = {"userId": 7}  # Ваш номер по журналу
    
    try:
        posts_response = requests.get("https://jsonplaceholder.typicode.com/posts", headers=headers, params=params)
        posts_response.raise_for_status()
        posts = posts_response.json()
        
        print(f"[V] Получено постов: {len(posts)}")
        print(f"[V] Заголовок первого поста: \"{posts[0]['title']}\"\n")
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Ошибка на этапе маскировки: {e}\n")
        return

    # ==========================================
    # ЭТАП 3: ПЕРЕДАЧА ДАННЫХ
    # ==========================================
    print("=== ЭТАП 3: ПЕРЕДАЧА ДАННЫХ ===")
    report_payload = {
        "name": target_name,
        "age": age,
        "gender": gender,
        "posts_count": len(posts)
    }
    
    try:
        post_response = requests.post("https://httpbin.org/post", json=report_payload)
        post_response.raise_for_status()
        
        server_answer = post_response.json()
        print("[V] Данные успешно отправлены. Подтверждение от сервера (поле json):")
        print(server_answer.get("json"))
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"[!]Ошибка при передаче данных: {e}\n")

    # ==========================================
    # ЭТАП 4: ЗАГРУЗКА УЛИК
    # ==========================================
    print("=== ЭТАП 4: ЗАГРУЗКА УЛИК ===")
    try:
        # stream=True позволяет скачивать большие файлы частями, не загружая их целиком в оперативную память
        img_response = requests.get("https://picsum.photos/400/300", stream=True)
        img_response.raise_for_status()
        
        with open("evidence.jpg", "wb") as file:
            for chunk in img_response.iter_content(chunk_size=8192):
                file.write(chunk)
                
        file_size = os.path.getsize("evidence.jpg")
        print(f"[V] Улика успешно сохранена как 'evidence.jpg'. Размер файла: {file_size} байт.\n")
        
    except requests.exceptions.RequestException as e:
        print(f"[!]Ошибка при загрузке улик: {e}\n")

    # ==========================================
    # ЭТАП 5: ОБРАБОТКА СБОЕВ
    # ==========================================
    print("=== ЭТАП 5: ОБРАБОТКА СБОЕВ ===")
    
    # Тест 1: Искусственная ошибка HTTP (404)
    print("Тест 1: Проверка обработки HTTP ошибки (404)...")
    try:
        bad_response = requests.get("https://httpbin.org/status/404")
        bad_response.raise_for_status()  # Этот метод генерирует HTTPError при кодах 4xx и 5xx
    except requests.exceptions.HTTPError:
        print("[!]Внимание: Сервер вернул ошибку HTTP (страница не найдена). Ресурс удален или доступ ограничен.\n")
    except requests.exceptions.RequestException as e:
        print(f"[!]Непредвиденная сетевая ошибка: {e}\n")

    # Тест 2: Искусственный таймаут
    print("🔹 Тест 2: Проверка обработки таймаута (задержка 6 сек, timeout=3)...")
    try:
        slow_response = requests.get("https://httpbin.org/delay/6", timeout=3)
        slow_response.raise_for_status()
    except requests.exceptions.Timeout:
        print("[!]Внимание: Превышено время ожидания ответа от сервера. Связь с базой нестабильна, цель могла заметить слежку.\n")
    except requests.exceptions.RequestException as e:
        print(f"[!]Непредвиденная сетевая ошибка: {e}\n")

    print("Миссия завершена. Скрипт завершил работу корректно.")

if __name__ == "__main__":
    main()