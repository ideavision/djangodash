import random
import string

def generate_random_string(length=16):
    source = string.digits + string.ascii_letters
    return ''.join(random.choice(source) for _ in range(length))