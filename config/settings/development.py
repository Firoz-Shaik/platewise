from .base import *

DEBUG = env.bool("DEBUG", default=True)

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# SQLite makes the project runnable immediately; set DATABASE_URL to a Supabase
# PostgreSQL connection string for a production-like environment.
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

ALLOWED_HOSTS = []
