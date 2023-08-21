from dotenv import load_dotenv
from os import environ

load_dotenv()

workers = 1
bind = f"127.0.0.1:{environ.get('PORT')}"
worker_class = f"uvicorn.workers.UvicornWorker"
