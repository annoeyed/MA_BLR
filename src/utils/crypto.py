import hashlib, hmac, secrets
def sha256(s:str)->str: return hashlib.sha256(s.encode()).hexdigest()
def hmac_sha256(key:str, msg:str)->str:
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()
def rand_token(n:int=16)->str: return secrets.token_hex(n)
