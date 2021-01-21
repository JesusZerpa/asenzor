import os,json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if not os.path.exists("config.json"):
    shutil.copy("config.example.json","config.json")
with open("config.json") as f:
    config=json.loads(f.read())

DATABASES = {
    'default': config["default"]
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT =os.path.join(BASE_DIR, 'media/')

ASENZOR_URL="/dashboard/"