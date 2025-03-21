import re
import random
import datetime
import pytz
import operator
import locale

locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

# Словарь шаблонов и ответов
responses = {
    r"привет|здравствуй": "Добрый день!",
    r"как тебя зовут\??": "Меня зовут Бот!",
    r"что ты умеешь\?": "Я умею отвечать на простые вопросы. Попробуй спросить: 'Как тебя зовут?', 'Какое сегодня число?' или 'Какая сегодня дата?'",
    r"какая сегодня дата\??": "Сегодня " + datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y'),
    r"какое сегодня число\??": "Сегодня " + datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d-е, %B'),
    r"сколько времени\??|который час\??": "Сейчас " + datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M'),
    r"какая сейчас погода\??": "Я пока не умею отвечать на этот вопрос.",
    r"посчитай|вычисли": "Введите выражение для вычисления, например: '2 + 2'.",
    r"спасибо": "Пожалуйста! Хотите спросить что-то еще?)",
}

# Функция для обработки арифметических операций
def calculate_expression(expression):
    try:
        # Используем регулярное выражение для извлечения чисел и оператора
        match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", expression)
        if not match:
            return "Не могу вычислить выражение."

        num1, op, num2 = match.groups()
        num1, num2 = int(num1), int(num2)

        # Словарь операций
        operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }

        if op in operations:
            result = operations[op](num1, num2)
            return str(result)
        else:
            return "Неизвестный оператор."
    except ZeroDivisionError:
        return "Ошибка: деление на ноль."
    except Exception as e:
        return f"Ошибка при вычислении: {e}"

# Функция для генерации ответа бота
def chatbot_response(text):
    text = text.lower()
    for pattern, response in responses.items():
        if re.search(pattern, text):
            if callable(response):
                return response()
            return response

    # Обработка арифметических выражений
    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", text):
        return calculate_expression(text)
    return random.choice(["Я не понял ваш вопрос.", "Попробуйте переформулировать."])

# Основной цикл работы бота
if __name__ == "__main__":
    print("Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            break
        print("Бот:", chatbot_response(user_input))