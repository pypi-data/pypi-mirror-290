### Installation
```bash
$ pip install django-aiohttp-rq
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_aiohttp_rq']

AIOHTTP_RQ_REDIS_HOST = 'localhost'
AIOHTTP_RQ_REDIS_PORT = 'aiohttp-rq-request-exception'
AIOHTTP_RQ_RESPONSE_QUEUE = 'aiohttp-rq-response'

# optional
AIOHTTP_RQ_RESTART_INTERVAL=600
AIOHTTP_RQ_SLEEP_INTERVAL=0.1 # 0.1 default

AIOHTTP_RQ_REQUEST_QUEUE = 'aiohttp-rq-request'
AIOHTTP_RQ_REQUEST_EXCEPTION_QUEUE = 'aiohttp-rq-request-exception'
AIOHTTP_RQ_RESPONSE_QUEUE = 'aiohttp-rq-response'
```
#### `migrate`
```bash
$ python manage.py migrate
```

### Features
+   based on [aiohttp-rq](https://pypi.org/project/aiohttp-rq)
+   push (`Request`)/pull (`RequestException`, `Response`) models
+   logging
    +   `logging.debug` messages
    +   `logging.conf` autoload (if exists)
+   `aiohttp_rq_bridge` worker command
    +   `aiohttp_rq_extra.py` extra command created by
+   admin

### Models
model|db_table|fields/columns
-|-|-
`Request`|`aiohttp_rq_request`|`id`,`worker`,`name`
`RequestException`|`aiohttp_rq_request_exception`|`id`,`url`,`method`,`data`,`headers`,`allow_redirects`,`max_redirects`
`Response`|`aiohttp_rq_response`|`id`,`url`,`status`,`headers`,`content_path`,`created_at`

### Management commands
name|description
-|-
`aiohttp_rq_bridge`|aiohttp_rq bridge worker
`aiohttp_rq_pull`|pull to `RequestException` and `Response`
`aiohttp_rq_push`|push `Request` to `AIOHTTP_RQ_REQUEST_QUEUE`
`aiohttp_rq_extra`|not implemented

### Examples
```bash
$ python manage.py aiohttp_rq_bridge
```

`aiohttp_rq_extra.py`
```python
# apps/aiohttp_rq_extra/management/commands/aiohttp_rq_extra.py
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('CALL aiohttp_rq_extra()')
```

