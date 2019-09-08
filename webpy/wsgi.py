import os
import sys


# add your project directory to the sys.path
# project_home = u'/home/bitdom8/webpy'
# if project_home not in sys.path:
#     sys.path.insert(0, project_home)


path = os.path.expanduser('~/GR')
if path not in sys.path:
    sys.path.append(path)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'webpy.settings'


# serve django via WSGI

# application = get_wsgi_application()
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
