whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace

__all__ = [
    'remove_punctuation',
    'remove_digits',
    'remove_whitespace',
    'remove_lowercase',
    'remove_uppercase',
    'remove_letters',
    'remove_printable',
    'remove_hexdigits',
    'remove_octdigits',
]

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', punctuation))

def remove_digits(text):
    return text.translate(str.maketrans('', '', digits))

def remove_whitespace(text):
    return text.translate(str.maketrans('', '', whitespace))

def remove_lowercase(text):
    return text.translate(str.maketrans('', '', ascii_lowercase))

def remove_uppercase(text):
    return text.translate(str.maketrans('', '', ascii_uppercase))

def remove_letters(text):
    return text.translate(str.maketrans('', '', ascii_letters))

def remove_printable(text):
    return text.translate(str.maketrans('', '', printable))

def remove_hexdigits(text):
    return text.translate(str.maketrans('', '', hexdigits))

def remove_octdigits(text):
    return text.translate(str.maketrans('', '', octdigits))
