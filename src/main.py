import uvicorn
from config import api_config

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=api_config["port"])
