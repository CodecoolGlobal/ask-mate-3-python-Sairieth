import time


def question_picker(question_id, questions):
    for question in questions:
        if question['id'] == question_id:
            return question


def get_time():
    return int(time.time())


def generate_id(questions):
    ids = []
    for question in questions:
        ids.append(question['id'])
    return max(ids) + 1
