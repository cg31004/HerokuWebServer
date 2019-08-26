
# https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'rtltw=9mx&ko!rzq4$2xf24!k4k)tqxj4z9l4^2pf4x^^=)!g)'

# change expired session (2 day)       <default 2 weeks>
COOKIE_TIME = 48*60*60

# only these urls are allowed users to GET or POST, '*' means all allowed
ALLOWED_HOSTS = ['*',]


#Line Token/secret ID
# LINE_CHANNEL_ACCESS_TOKEN = "M1xTOuceNrJBTr9DjuC083k1fOfZqy9wL3U8QJmBlsJcelYsV+PEvLjk9gVG73oB6SR2E1sBkgpchKEV0G9EvQG7a8n+10H/J1BR3REvoiCsnfeoV5Taqti8zL8Nwe0FIIamlOurDgxbACKHtDeKAQdB04t89/1O/w1cDnyilFU="
# LINE_CHANNEL_SECRET = "31807d71b57007b90bc7c5db995b5d9f"

# LINE_CHANNEL_ACCESS_TOKEN = "H/TyoEmynIY4hptT7NEtoZ0dVHqoCbypzqVqCMg3jtFtpUb50ZBOV4ECoegp6QjUd0qZe7d4jc0r6WzgMIjx++o5LvWCcTWL1YMOciLQNOBjd612WHVZvg0a3OS52LmshZLAI36Na118F3WSBljM7gdB04t89/1O/w1cDnyilFU="
# LINE_CHANNEL_SECRET = "8e94eb108a14671ae432e1fe6f8133e4"

LINE_CHANNEL_ACCESS_TOKEN = "zL34/M8A4fqFocLtpOwfvtiBNxQIsqd2vxJMRShrAscAKcnHjTiXHmrf84Ny/Tsj4uXsmwGaugDAX4tcWL5Q7hrQNuA+SCEB+nYDN89g1NH20HiocajSY8FFDubHlYHNYq2Ri2Om0N8pxD7qTN8acQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "a16c5c4454477ca7f580e73a2f93f2b0"

import os
if 'DYNO' in os.environ:
    
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')