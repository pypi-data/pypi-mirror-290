# ByteCaptcha3/utils.py

import random
import string
import re

def generate_russian_text(length=6):
    """Генерация текста CAPTCHA на русском языке."""
    russian_characters = 'абвгдеёжзийклмнопрстуфхцчшщыэюя'
    return ''.join(random.choice(russian_characters) for _ in range(length))

def generate_math_problem():
    """Генерация простой математической задачи для CAPTCHA."""
    operations = ['+', '-']
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(operations)
    if operation == '+':
        answer = num1 + num2
    else:
        answer = num1 - num2
    problem = f"{num1} {operation} {num2} = ?"
    return problem, answer

def add_math_to_captcha(captcha_text):
    """Добавление математической задачи к тексту CAPTCHA."""
    problem, answer = generate_math_problem()
    return f"{captcha_text} | {problem}", answer

def validate_math_solution(problem, answer, user_answer):
    """Проверка правильности ответа на математическую задачу."""
    return user_answer == answer
