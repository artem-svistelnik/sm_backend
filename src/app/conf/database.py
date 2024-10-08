import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "HOST": os.environ.get("DB_HOST", "database"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres123456"),
        "CONN_HEALTH_CHECKS": True,
    }
}
