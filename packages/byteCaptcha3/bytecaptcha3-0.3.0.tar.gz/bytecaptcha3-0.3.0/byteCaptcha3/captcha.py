# ByteCaptcha3/captcha.py

from PIL import Image, ImageDraw, ImageFont
import random
from .utils import generate_russian_text, add_math_to_captcha, validate_math_solution

class CaptchaGen:
    def __init__(self, width=200, height=70, font_size=36):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font = ImageFont.load_default()

    def generate_text(self, length=6):
        """Генерация текста CAPTCHA (русский текст)."""
        return generate_russian_text(length)

    def create_captcha(self, text):
        """Создание изображения CAPTCHA на основе текста и задачи."""
        # Добавление математической задачи к тексту
        captcha_text, math_answer = add_math_to_captcha(text)
        
        # Создание изображения CAPTCHA
        image = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(captcha_text, font=self.font)
        text_x = (self.width - text_width) / 2
        text_y = (self.height - text_height) / 2
        draw.text((text_x, text_y), captcha_text, fill=(0, 0, 0), font=self.font)

        # Добавление шума (простое примечание)
        for _ in range(random.randint(100, 200)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=(0, 0, 0))

        return image, math_answer
