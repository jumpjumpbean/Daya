# Gunicorn config file

import os

bind='0.0.0.0:5000'
workers=3
backlog=2048
worker_class="gevent" #sync, gevent,meinheld
debug=True
proc_name='gunicorn.pid'
pidfile='/var/www/debug.log'
loglevel='debug'
