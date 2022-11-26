from hashlib import sha256


def make_hash(s: str):
    return sha256(s.encode("utf-8")).hexdigest()


def check_hash(hash_digest: str, s: str):
    return hash_digest == make_hash(s)
