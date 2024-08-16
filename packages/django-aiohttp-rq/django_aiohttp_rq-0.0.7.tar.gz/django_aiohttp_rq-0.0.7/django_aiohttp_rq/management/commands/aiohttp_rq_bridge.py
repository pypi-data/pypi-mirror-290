import logging
import os
import sys
import time

from django.conf import settings
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand
from django.db import connection

from ...models import Request

COMMAND2APP = {command:app for command,app in get_commands().items()}
RESTART_INTERVAL = getattr(settings,'AIOHTTP_RQ_RESTART_INTERVAL',None)
SLEEP_INTERVAL = getattr(settings,'SLEEP_INTERVAL',0.1) or 0.1
RESTART_AT = None
if RESTART_INTERVAL:
    RESTART_AT = time.time()+RESTART_INTERVAL

class Command(BaseCommand):
    def handle(self, *args, **options):
        if os.path.exists('logging.conf'):
            logging.config.fileConfig('logging.conf')
        while not RESTART_AT or time.time()<RESTART_AT:
            if Request.objects.only('id').first():
                call_command('aiohttp_rq_push')
            call_command('aiohttp_rq_pull')
            if 'aiohttp_rq_extra' in COMMAND2APP:
                call_command('aiohttp_rq_extra')
            time.sleep(0.1)
