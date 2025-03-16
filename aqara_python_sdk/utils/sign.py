import hashlib


def sign(token, appid, keyid, appkey, timestamp, nonce):
    if token is not None:
        data = f"Accesstoken={token}&Appid={appid}&Keyid={keyid}&Nonce={nonce}&Time={timestamp}"
    else:
        data = f"Appid={appid}&Keyid={keyid}&Nonce={nonce}&Time={timestamp}"
    data += appkey
    data = data.lower()
    # 对data进行md5 32位加密
    md5 = hashlib.md5()
    md5.update(data.encode())
    return md5.hexdigest()
