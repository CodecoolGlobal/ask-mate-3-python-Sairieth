from data_manager import get_saved_data


def question_picker(question_id, questions):
    for question in questions:
        if question['id'] == question_id:
            return question
