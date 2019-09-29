import os,sys

sys.path.insert(0, '/home/m/mdrevivru/public_html')
sys.path.insert(0, '/home/m/mdrevivru')
sys.path.insert(0, '/home/m/mdrevivru/ispu_env/lib64/python2.7/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "aes.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
