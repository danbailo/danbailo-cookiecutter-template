from functools import partial


def obfuscate(text: str, safe_size: int = 10, obfuscate_char: str = '*') -> str:
    safe_text = text[:safe_size]
    return safe_text + obfuscate_char * abs(len(text) - len(safe_text))


obfuscate_document = partial(obfuscate, safe_size=5)
obfuscate_name = partial(obfuscate, safe_size=15)
