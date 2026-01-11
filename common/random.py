import hashlib

def fixed_length_from_key(key: str, length: int) -> str:
    h = hashlib.sha256(key.encode()).hexdigest()
    digits = str(int(h, 16))
    return digits[:length]
