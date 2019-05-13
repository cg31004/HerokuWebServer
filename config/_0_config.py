import os


# https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'rtltw=9mx&ko!rzq4$2xf24!k4k)tqxj4z9l4^2pf4x^^=)!g)'

# change expired session (2 day)       <default 2 weeks>
COOKIE_TIME = 48*60*60

# only these urls are allowed users to GET or POST, '*' means all allowed
ALLOWED_HOSTS = ['*',]

