from __future__ import annotations

from celery_app import add

if __name__ == "__main__":
    # Call the task asynchronously
    result = add.delay(4, 6)

    # Check if the task is completed and get the result
    print(f"Task ID: {result.id}")
    print(f"Task Status: {result.status}")
    print(f"Task Result: {result.get()}")
