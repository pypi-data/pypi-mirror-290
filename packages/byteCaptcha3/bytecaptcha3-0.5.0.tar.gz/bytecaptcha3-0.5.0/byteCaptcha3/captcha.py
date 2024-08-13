# ByteCaptcha3/captcha.py

from PIL import Image, ImageDraw, ImageFont
import random
from .utils import generate_russian_text, add_math_to_captcha, validate_math_solution

class CaptchaGen:
    def __init__(self, font_size=36, width=200, height=70, noise_level=5):
        self.font_size = font_size
        self.width = width
        self.height = height
        self.noise_level = noise_level
        self.font = ImageFont.truetype("arial.ttf", self.font_size)

    def generate_text(self, length=6, use_russian=False):
        """Генерация случайного текста для CAPTCHA"""
        if use_russian:
            return generate_russian_text(length)
        else:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def add_noise(self, draw):
        """Добавление шума на изображение"""
        for _ in range(self.noise_level):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0), width=1)

    def create_captcha(self, captcha_text=None, use_russian=False, math_captcha=False):
        """Создание изображения CAPTCHA"""
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        if math_captcha:
            captcha_text, answer = add_math_to_captcha()
        else:
            answer = None
            if captcha_text is None:
                captcha_text = self.generate_text(length=6, use_russian=use_russian)

        # Получение размеров текста с использованием textbbox
        text_bbox = draw.textbbox((0, 0), captcha_text, font=self.font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Центрирование текста на изображении
        text_x = (self.width - text_width) // 2
        text_y = (self.height - text_height) // 2

        draw.text((text_x, text_y), captcha_text, font=self.font, fill=(0, 0, 0))

        # Добавление шума
        self.add_noise(draw)

        return image, answer

