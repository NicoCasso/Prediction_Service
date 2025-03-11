# Gunicorn configuration file
import multiprocessing
from core.config  import API_CLIENT_ADDRESS, API_INTERNAL_PORT

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = f"{API_CLIENT_ADDRESS}:{API_INTERNAL_PORT}"

worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1