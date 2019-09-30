





import os

# change expired session (2 day)       <default 2 weeks>
COOKIE_TIME = 48*60*60

# only these urls are allowed users to GET or POST, '*' means all allowed
ALLOWED_HOSTS = ['*',]

if 'DYNO' in os.environ:
    SECRET_KEY = os.environ.get('Django_SecretKey')
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

else :
    from .local_config import (SECRET_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET)

    SECRET_KEY = SECRET_KEY
    LINE_CHANNEL_ACCESS_TOKEN = LINE_CHANNEL_ACCESS_TOKEN
    LINE_CHANNEL_SECRET = LINE_CHANNEL_SECRET
    