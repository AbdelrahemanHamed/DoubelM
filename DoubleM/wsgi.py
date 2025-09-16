import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DoubleM.settings")  # replace DoubelM with your project folder name

application = get_wsgi_application()
