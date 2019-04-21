import random
import string


def randstr(chars=string.ascii_lowercase + string.digits, len=16) -> str:
    return ''.join(random.choices(chars, k=len))
