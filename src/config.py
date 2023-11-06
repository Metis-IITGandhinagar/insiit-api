import os


def get_config():
    app_config = {
        "api": {
            "port": int(os.getenv("API_PORT")),
            "api-keys": eval(os.getenv("API_KEYS")),
            "admin-api-key": os.getenv("ADMIN_API_KEY"),
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

with open("./assets/app_description.md", "r") as f:
    app_description = f.read()

tags_metadata = [
    {
        "name": "Hello World!",
        "description": "<font size='4'>Just a simple Hello World! endpoint</font>",
    },
    {
        "name": "Mess",
        "description": "<font size='4'>Endpoints related to Mess</font>",
    },
    {
        "name": "Food Outlets",
        "description": "<font size='4'>Endpoints related to Food Outlets</font>",
    },
    {
        "name": "[ADMIN] Mess",
        "description": "<font size='4'>Admin endpoints related to Mess - POST, PUT, DELETE</font>",
    },
    {
        "name": "[ADMIN] Food Outlets",
        "description": "<font size='4'>Admin endpoints related to Food Outlets - POST, PUT, DELETE</font>",
    },
]
