"""
WSGI config for miika project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

# Comment out for local
this_file = "venv/bin/activate_this.py"
exec(open(this_file).read(), {'__file__': this_file})

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miika.settings')

application = get_wsgi_application()
