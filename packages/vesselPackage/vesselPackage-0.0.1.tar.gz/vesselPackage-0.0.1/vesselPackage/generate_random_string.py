import random
import string

def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
