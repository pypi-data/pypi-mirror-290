# ByteCaptcha3/utils.py
import random

def generate_russian_text(length=6):
    """Генерация случайного текста на русском языке для CAPTCHA."""
    russian_chars = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return ''.join(random.choices(russian_chars, k=length))

def add_math_to_captcha(captcha_text):
    """Добавление математического выражения к тексту капчи."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])
    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    return f"{captcha_text} {question} =", answer

def validate_math_solution(expected_answer, user_input):
    """Проверка правильности ответа на математическую задачу."""
    try:
        return int(user_input) == expected_answer
    except ValueError:
        return False
