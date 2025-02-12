from __future__ import annotations

from celery import Celery

# Create a Celery instance
app = Celery("tasks", broker="redis://localhost:6379/0")

# Configuring backend for storing task results (optional)
app.conf.result_backend = "redis://localhost:6379/0"


# Define a simple Celery task
@app.task
def add(x, y):
    return x + y
