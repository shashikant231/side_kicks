from flask import Flask, request, jsonify
from celery import Celery
import time
import json

celery = Celery(
    "__name__",
    broker="pyamqp://guest@localhost//",
    backend="redis://127.0.0.1:6379/0",
)


app = Flask(__name__)


@app.route("/divide", methods=["POST"])
def divide_api():
    data = json.loads(request.data)
    num1 = data.get("nums1")
    num2 = data.get("nums2")
    # time consuming task
    task = divide.delay(num2, num1)
    return jsonify(
        {
            "status": task.state,
            "result": task.result if task.state == "SUCCESS" else None,
        }
    )
    # return f"Task Completed : {task.result}"


# defined a task with name : divide_two_num
@celery.task(name="divide_two_num")
def divide(a, b):
    time.sleep(5)
    return a / b
