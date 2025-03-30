import re
import random
import datetime
import pytz
import operator
import locale
import requests
import webbrowser

API_KEY = "95f43803daee41f68c348dbed7b7cc3d"
locale.setlocale(locale.LC_ALL, "Russian")

# Функция погоды
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"В городе {city} сейчас {weather_desc} при температуре {temp}°C."
    else:
        return "Не удалось получить информацию о погоде. Попробуйте другой город."

# Функция обработки математических выражений
def calculate_expression(expr):
    try:
        operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", expr.strip())
        if not match:
            return "Неверный формат выражения"

        num1 = int(match.group(1))
        operator_symbol = match.group(2)
        num2 = int(match.group(3))

        if operator_symbol not in operations:
            return f"Неподдерживаемый оператор: {operator_symbol}"

        result = operations[operator_symbol](num1, num2)

        if operator_symbol == '/':
            if num2 == 0:
                return "Ошибка: деление на ноль"
            return str(int(result)) if result.is_integer() else str(round(result, 2))

        return str(int(result)) if isinstance(result, float) and result.is_integer() else str(result)

    except Exception as e:
        return f"Ошибка вычисления: {str(e)}"

# Функция поиска в интернете (Google)
def search_web(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Результаты поиска по запросу: '{query}'"

responses = {
    r"привет|здравствуй": ["Добрый день!", "Приветствую!", "Здравствуйте!"],
    r"как тебя зовут\??": ["Меня зовут Бот!", "Я - ваш виртуальный помощник"],

    r"как дела\??": [
        "Спасибо, у меня всё хорошо!",
        "Неплохо, а у тебя?",
        "Я просто программа, но чувствую себя отлично!"
    ],
    r"что ты умеешь\??": [
        "Я могу отвечать на вопросы, искать информацию и выполнять команды!",
        "Мои возможности: погода, вычисления, поиск в интернете и многое другое.",
        "Спросите о погоде, времени или попросите что-то посчитать."
    ],

    r"погода в (.+)": lambda city: get_weather(city.strip()),
    r"поиск\s+(.+)": lambda query: search_web(query.strip()),
    r"посчитай (.+)": lambda expr: calculate_expression(expr),

    r"какая сегодня дата\??": lambda: datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
    r"который час|сколько время\??": lambda: datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M'),

    r"пока|выход": ["До свидания!", "Буду рад помочь снова!", "Всего хорошего!"]
}

def chatbot_response(text):
    text = text.lower().strip()

    if re.fullmatch(r"\d+\s*[\+\-\*/]\s*\d+", text):
        return calculate_expression(text)

    # Поиск совпадений с шаблонами
    for pattern, response_options in responses.items():
        if match := re.search(pattern, text, re.IGNORECASE):
            if callable(response_options):
                return response_options(*match.groups()) if match.groups() else response_options()
            return random.choice(response_options) if isinstance(response_options, list) else response_options

    return random.choice([
        "Извините, я не понял ваш вопрос",
        "Можете переформулировать запрос?",
        "Я могу помочь с погодой, вычислениями или поиском в интернете"
    ])

# Функция логирования диалога
def log_dialog(user_input, bot_response):
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Пользователь: {user_input}\n")
        log_file.write(f"Бот: {bot_response}\n")
        log_file.write("-" * 40 + "\n")


if __name__ == "__main__":
    open("chat_log.txt", "w")
    print("Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            log_dialog(user_input, "До свидания!")
            break
        bot_response = chatbot_response(user_input)
        print("Бот:", bot_response)
        log_dialog(user_input, bot_response)
