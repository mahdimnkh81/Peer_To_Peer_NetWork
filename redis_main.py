import redis

redis_host = 'localhost'
redis_port = 6379


def redis_string():
    try:

        r = redis.StrictRedis(host = redis_host, port=redis_port, decode_responses=True)
        r.rpush("vvv",1921,897,1235,528)
        while r.llen("vvv") != 0:
            print(r.rpop("vvv"))
        r.set("message", "mahdi")
        msg = r.get("message")
        print(msg)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    redis_string()
