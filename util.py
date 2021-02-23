import time


def question_picker(question_id, questions):
    for question in questions:
        if question['id'] == question_id:
            return question


def get_time():
    return int(time.time())


def generate_id(questions):
    ids = []
    for question in questions[1:]:
        ids.append(question['id'])
    max_id = max(ids)
    return int(max_id) + 1


def create_new_question(title, message, questions):
    new_question = {'id': generate_id(questions), 'submission_time': get_time(), 'view_number': 0, 'vote_number': 0,
                    'title': title, 'message': message}
    return new_question
