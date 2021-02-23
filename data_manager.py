import csv
import os

file_path_questions = os.getenv('file_path') if 'file_path' in os.environ else 'sample_data/question.csv'
file_path_answers = os.getenv('file_path') if 'file_path' in os.environ else 'answers.csv'
questions_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id', 'submission_time', 'vote_number', 'questions_id', 'message', 'image']


def get_saved_data(file_path, header):
    with open(file_path, newline='') as csvfile:
        csv_data = csv.DictReader(csvfile, fieldnames=header, restval="")
        saved_data = []
        for rows in csv_data:
            saved_data.append(rows)
            # temp_dict = {}
            # for key, value in rows.items():
            #     temp_dict[key] = value
            # question_data.append(temp_dict)
        return saved_data


def write_to_file(file_path, header):
    with open(file_path, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)


def sort_questions(data, sort_key):
    sorted_questions = sorted(data, key=lambda k: k[sort_key], reverse=True)
    return sorted_questions
