import os
from .settings import ALLOWED_HOSTS, BASE_DIR

ALLOWED_HOSTS=[os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS=['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG=False
