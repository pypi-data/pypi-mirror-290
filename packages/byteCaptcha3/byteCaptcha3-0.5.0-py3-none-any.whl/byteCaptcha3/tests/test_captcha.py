# tests/test_captcha.py

import unittest
from byteCaptcha3.captcha import CaptchaGen

class TestCaptcha(unittest.TestCase):
    def test_generate_captcha(self):
        generator = CaptchaGenerator()
        image = generator.create_captcha()
        self.assertIsNotNone(image)
        image.show()  # Для отладки

if __name__ == "__main__":
    unittest.main()
