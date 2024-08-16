import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django_aiohttp_rq.redis_client import REDIS

from ...models import RequestException, Response

PREFETCH_COUNT = 1000
REQUEST_EXCEPTION_QUEUE = getattr(settings,'AIOHTTP_RQ_REQUEST_EXCEPTION_QUEUE','aiohttp_rq_request_exception')
RESPONSE_QUEUE = getattr(settings,'AIOHTTP_RQ_RESPONSE_QUEUE','aiohttp_rq_response')


def get_data_list(REDIS,queue):
    pipe = REDIS.pipeline()
    pipe.lrange(queue, 0, PREFETCH_COUNT - 1)  # Get msgs (w/o pop)
    pipe.ltrim(queue, PREFETCH_COUNT, -1)  # Trim (pop) list to new value
    value_list, trim_success = pipe.execute()
    if value_list:
        logging.debug('REDIS PULL %s (%s)' % (queue,len(value_list)))
        return list(map(lambda s:json.loads(s),value_list))

class Command(BaseCommand):
    def handle(self, *args, **options):
        bulk_create_list = []
        for data in get_data_list(REDIS,REQUEST_EXCEPTION_QUEUE) or []:
            bulk_create_list += [RequestException(
                url=data['url'],
                exc_class=str(data['exc_class']),
                exc_message=str(data['exc_message'])
            )]
        for data in get_data_list(REDIS,RESPONSE_QUEUE) or []:
            bulk_create_list += [Response(
                url=str(data['url']),
                status=int(data['status']),
                headers = data['headers'],
                content_path = data['content_path']
            )]
        for model in set(map(type,bulk_create_list)):
            _bulk_create_list = list(filter(
                lambda i:isinstance(i,model),
                bulk_create_list
            ))
            count = len(_bulk_create_list)
            logging.debug('BULK CREATE %s (%s)' % (model._meta.db_table,count))
            model.objects.bulk_create(_bulk_create_list)
