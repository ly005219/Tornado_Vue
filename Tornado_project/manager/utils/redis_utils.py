import redis
def save_code(email,code):
    client=redis.Redis(host='localhost',port=6379,db=0)
    client.set(email,code)

def get_code(email):
    client=redis.Redis(host='localhost',port=6379,db=0)
    code=client.get(email)
    if code:
        return code.decode('utf-8')
    else:
        return None