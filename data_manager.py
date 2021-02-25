import csv
import os

file_path_questions = os.getenv('file_path') if 'file_path' in os.environ else f"{os.path.dirname(__file__)}/sample_data/question.csv"
file_path_answers = os.getenv('file_path') if 'file_path' in os.environ else f"{os.path.dirname(__file__)}/sample_data/answer.csv"
questions_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_saved_data(file_path, header):
    with open(file_path, newline='') as csvfile:
        csv_data = csv.DictReader(csvfile, fieldnames=header, restval="")
        saved_data = []
        for rows in csv_data:
            saved_data.append(rows)
        return saved_data


def write_to_file(file_path, header, new_dictionary):
    with open(file_path, "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, restval="")
        writer.writerow(new_dictionary)


def update_file(file_path, header, questions):
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, restval="")
        writer.writeheader()
        for question in questions:
            writer.writerow(question)


def sort(data, sort_key, direction):
    if direction == "descending":
        if sort_key in ["submission_time", "view_number", "vote_number"]:
            sorted_questions = sorted(data, key=lambda k: int(k[sort_key]), reverse=True)
            return sorted_questions
        elif sort_key in ["message", "title"]:
            sorted_questions = sorted(data, key=lambda k: k[sort_key], reverse=True)
            return sorted_questions
    elif direction == "ascending":
        if sort_key in ["submission_time", "view_number", "vote_number"]:
            sorted_questions = sorted(data, key=lambda k: int(k[sort_key]))
            return sorted_questions
        elif sort_key in ["message", "title"]:
            sorted_questions = sorted(data, key=lambda k: k[sort_key])
            return sorted_questions


def delete_question_from_file(question_id):
    questions = get_saved_data(file_path_questions, header=questions_header)[1:]
    for question in questions:
        if question["id"] == question_id:
            index = questions.index(question)
            del questions[index]
    update_file(file_path_questions, questions_header, questions)


def delete_answer_from_file(question_id):
    answers = get_saved_data(file_path_answers, header=answer_header)[1:]
    for _ in range(len(answers)):
        for answer in answers:
            if answer["question_id"] == question_id:
                index = answers.index(answer)
                del answers[index]
    update_file(file_path_answers, answer_header, answers)
