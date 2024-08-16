import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django_aiohttp_rq.redis_client import REDIS

from ...models import Request

REQUEST_QUEUE = getattr(settings,'AIOHTTP_RQ_REQUEST_QUEUE','aiohttp_rq_request')

class Command(BaseCommand):
    def handle(self, *args, **options):
        request_list = list(Request.objects.all()[0:10000])
        if request_list:
            data_list = []
            for request in request_list:
                data_list+=[dict(
                    id=request.id,
                    url=request.url,
                    method=request.method,
                    headers=request.headers,
                    data=request.data,
                    allow_redirects=request.allow_redirects
                )]
            logging.debug('REDIS PUSH %s (%s)' % (REQUEST_QUEUE,len(request_list)))
            pipe = REDIS.pipeline()
            for data in data_list:
                REDIS.lpush(REQUEST_QUEUE, json.dumps(data))
            pipe.execute()
            Request.objects.filter(
                id__in=list(map(lambda r:r.id,request_list))
            ).delete()
