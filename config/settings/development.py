from .base import *

# Preserve the existing local PostgreSQL configuration while allowing a single
# DATABASE_URL (for Supabase and other managed PostgreSQL providers) in hosted
# environments.
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=True)

database_url = env("DATABASE_URL", default="")
if database_url:
    DATABASES = {"default": env.db("DATABASE_URL")}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
