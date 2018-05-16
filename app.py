from flask import Flask, jsonify
from tasks import task_test
from celery.result import AsyncResult

import time


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# @app.route('/test')
# def show_test():
#     # celery task connection
#     return task_test.is_celery_working()
#
#
# @app.route('/tests/<ddd>')
# def show_tests(ddd):
#     # celery task connection
#     print(1)
#     res = AsyncResult(ddd)
#     print(2)
#     res.state
#     print(3)
#     res.get()
#     # print(.get())
#     # print('a271f018-e0d8-4492-8ce2-373aa8de979b')
#     return task_test.is_celery_working()


# connect celery instance to flask instance
@app.route('/multiple/<a>/<b>')
def apply_multiple(a, b):
    print(1)
    print(a, b)

    multiple_task_id = task_test.multiple.delay(3, 4)
    print(2)
    print(multiple_task_id)
    if multiple_task_id:
        print(3)
        print(multiple_task_id.status)
        task_test.is_celery_working()
        # print(4)
        # print(multiple_task_id.get())
        # multiple_task_id.get()
        # multiple_task_result = task_test.multiple.AsyncResult(multiple_task_id)
        # print(multiple_task_result.get())
    #     # multiple_task_state = multiple_task_id.state
    # if multiple_task_state == 'PENDING':
    #     return

    # return f"task_id is {multiple_task_id} and task_result is {str(multiple_task_result.get)}"
    # return f"<a href=\"http://0.0.0.0:5000/{str(multiple_task_id)}\">{str(multiple_task_id)}</a>"
    return str(multiple_task_id)


# show celery result
@app.route('/<multiple_task_id>')
def show_multiple_result(multiple_task_id):
    multiple_task_id = task_test.multiple.AsyncResult(multiple_task_id)
    if multiple_task_id.state == 'PENDING':
        # job did not start yet
        response = {
            'state': multiple_task_id.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif multiple_task_id.state != 'FAILURE':
        response = {
            'state': multiple_task_id.state,
            'current': multiple_task_id.info
        }
    else:
        # something went wrong in the background job
        response = {
            'state': multiple_task_id.state,
            'current': 1,
            'total': 1,
            'status': str(multiple_task_id.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
