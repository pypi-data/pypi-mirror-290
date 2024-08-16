from django.conf import settings
import redis

REDIS_HOST = settings.AIOHTTP_RQ_REDIS_HOST
REDIS_PORT = settings.AIOHTTP_RQ_REDIS_PORT
REDIS_DB = settings.AIOHTTP_RQ_REDIS_DB
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
