import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(secret_id, backup=None):
    return os.getenv(secret_id, backup)

# Keep at the end
if get_secret('ENVIRONMENT') == 'production':
    from .production import *
else:
    from .dev import *
