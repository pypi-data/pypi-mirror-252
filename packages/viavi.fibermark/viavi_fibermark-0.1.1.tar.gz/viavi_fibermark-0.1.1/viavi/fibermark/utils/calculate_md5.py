import hashlib


def md5(filename: str) -> str:
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        # reading chunks of 4096 bytes sequentially in case of not enough memory for whole file reading
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
