# byteCaptcha3/utils.py

import random

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))
