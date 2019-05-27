import redis

redis_server = '192.168.163.171'
redis_client = redis.Redis(host=redis_server, port=6379, decode_responses=True)