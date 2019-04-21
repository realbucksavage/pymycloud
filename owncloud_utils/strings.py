import random
import string


def randstr(chars=string.ascii_lowercase + string.digits, len=16) -> str:
    """Generates a random string out of given charactes.

    Parameters
    ----------
    chars : type
        An array if charaters to generate the string from.
    len : type
        Length of the string.

    Returns
    -------
    str
        A random string of length `len`.

    """
    return ''.join(random.choices(chars, k=len))
