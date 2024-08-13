# byteCaptcha3/noise.py

from PIL import ImageDraw
import random

def add_noise(image, level=1):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for _ in range(int(level * 10)):
        # Рисуем случайные линии
        start_point = (random.randint(0, width), random.randint(0, height))
        end_point = (random.randint(0, width), random.randint(0, height))
        draw.line([start_point, end_point], fill=random.choice(['black', 'gray']), width=random.randint(1, 3))

    return image
