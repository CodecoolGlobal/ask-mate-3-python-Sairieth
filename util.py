import time


def question_picker(question_id, questions):
    for question in questions:
        if question['id'] == question_id:
            return question


def get_time():
    return int(time.time())
