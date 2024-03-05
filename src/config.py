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

# with open("./assets/static/styles.css", "r") as f:
#     styles = f.read()

tags_metadata = [
    {
        "name": "hello world!",
        "description": '<font size="4">A simple "Hello World" endpoint</font>',
    },
    {
        "name": "mess",
        "description": "<font size='4'>Everything about the messes at IITGN</font>",
    },
    {
        "name": "food outlets",
        "description": "<font size='4'>Everything about the different food outlets at IITGN</font>",
    },
    {
        "name": "bus",
        "description": "<font size='4'>Everything about the bus schedule at IITGN</font>",
    },
    {
        "name": "[admin] mess",
        "description": "<font size='4'>Admin endpoints for manipulating data of messes</font>",
    },
    {
        "name": "[admin] food outlets",
        "description": "<font size='4'>Admin endpoints for manipulating data of food outlets</font>",
    },
    {
        "name": "[admin] bus",
        "description": "<font size='4'>Admin endpoints for manipulating data of bus schedule</font>",
    },
]
