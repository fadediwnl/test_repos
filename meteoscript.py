import requests
import sys

WEATHER_CODES = {
    0: "☀️ Ясно", 1: "🌤️ Преимущественно ясно", 2: "⛅️ Переменная облачность",
    3: "☁️ Пасмурно", 45: "🌫️ Туман", 48: "🌫️ Иней", 51: "🌦️ Легкая морось",
    53: "🌦️ Морось", 55: "🌧️ Сильная морось", 61: "🌧️ Небольшой дождь",
    63: "🌧️ Дождь", 65: "🌧️ Сильный дождь", 71: "🌨️ Небольшой снег",
    73: "🌨️ Снег", 75: "🌨️ Сильный снег", 80: "🌦️ Ливень",
    95: "⛈️ Гроза", 96: "⛈️ Гроза с градом"
}

def get_city_coordinates(city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru"
    print(f"[Диагностика] Запрос координат: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            return None
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети при геокодировании: {e}")
        sys.exit(1)
    except requests.exceptions.JSONDecodeError:
        print("❌ Ошибка: Получен невалидный JSON от сервера геокодирования.")
        sys.exit(1)

def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto"
    print(f"[Диагностика] Запрос погоды: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("current", {})
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети при получении погоды: {e}")
        sys.exit(1)
    except requests.exceptions.JSONDecodeError:
        print("❌ Ошибка: Получен невалидный JSON от сервера погоды.")
        sys.exit(1)

def decode_weather_code(code: int):
    return WEATHER_CODES.get(code, f"Неизвестные условия (код: {code})")

def format_weather_output(city: str, weather_data: dict):
    temp = weather_data.get("temperature_2m", "N/A")
    humidity = weather_data.get("relative_humidity_2m", "N/A")
    wind_speed = weather_data.get("wind_speed_10m", "N/A")
    weather_code = weather_data.get("weather_code", "N/A")
    
    weather_desc = decode_weather_code(weather_code)
    temp_str = f"+{temp:.0f}°C" if isinstance(temp, (int, float)) and temp > 0 else f"{temp}°C"
    
    return (
        f"\nПогода в городе: {city}\n"
        f"{'Температура:':<15}{temp_str}\n"
        f"{'Влажность:':<15}{humidity}%\n"
        f"{'Ветер:':<15}{wind_speed} км/ч\n"
        f"{'Состояние:':<15}{weather_desc}"
    )

def main():
    city_name = input("Введите название города на английском: ").strip()
    if not city_name:
        print("Ошибка: Название города не может быть пустым.")
        sys.exit(1)
        
    coordinates = get_city_coordinates(city_name)
    if not coordinates:
        print(f"Город '{city_name}' не найден. Проверьте название.")
        sys.exit(1)
        
    weather_data = get_weather(*coordinates)
    if not weather_data:
        print("Не удалось получить данные о погоде.")
        sys.exit(1)
        
    print(format_weather_output(city_name, weather_data))

if __name__ == "__main__":
    main()