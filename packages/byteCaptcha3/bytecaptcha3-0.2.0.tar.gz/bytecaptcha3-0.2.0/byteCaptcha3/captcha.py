# byteCaptcha3/captcha.py

import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .noise import add_noise
from .utils import random_color

class CaptchaGen:
    def __init__(self, width=200, height=70, font_size=36, font_path="fonts/default.ttf"):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font = ImageFont.truetype(font_path, font_size)

    def generate_text(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_captcha(self, text=None, noise_level=1, background_color=None):
        if text is None:
            text = self.generate_text()

        if background_color is None:
            background_color = random_color()

        # Создаем базовое изображение
        image = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(text, font=self.font)
        text_position = ((self.width - text_width) // 2, (self.height - text_height) // 2)
        draw.text(text_position, text, font=self.font, fill=random_color())

        # Добавление шума
        image = add_noise(image, noise_level)

        # Размытие (если необходимо)
        image = image.filter(ImageFilter.GaussianBlur(1))

        return image

    def save_captcha(self, image, path):
        image.save(path)
