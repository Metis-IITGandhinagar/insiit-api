import os


def get_config():
    app_config = {
        "api": {
            "port": int(os.getenv("API_PORT")),
            "api-keys": eval(os.getenv("API_KEYS")),
        },
        "db": {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT")),
            "username": os.getenv("DB_USERNAME"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_DATABASE"),
        },
    }

    return app_config


config = get_config()
api_config = config["api"]
db_config = config["db"]
