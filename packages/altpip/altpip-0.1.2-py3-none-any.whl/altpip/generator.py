from string import ascii_letters, ascii_lowercase, ascii_uppercase
from random import choices

def generate(count: int = 16):
    return ''.join(choices(ascii_letters+ascii_lowercase+ascii_uppercase+"1234567890_-=+:;"))