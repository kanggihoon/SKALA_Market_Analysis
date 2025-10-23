def safe_get(dct, key, default=None):
    return dct.get(key, default) if isinstance(dct, dict) else default

