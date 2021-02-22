import csv
import os
from random import randint

file_path_questions = os.getenv('file_path') if 'file_path' in os.environ else 'questions.csv'
file_path_answers = os.getenv('file_path') if 'file_path' in os.environ else 'answers.csv'
questions_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
questions_header = ['id', 'submission_time', 'vote_number', 'questions_id', 'message', 'image']

def get_all_user_story(file_path):
    with open(file_path, newline='') as csvfile:
        csv_data = csv.DictReader(csvfile)
        user_data = {}
        for rows in csv_data:
            temp_dict = {}

            for key, value in rows.items():
                if key == "id":
                    id = value
                else:
                    temp_dict[key] = value
            user_data[id] = temp_dict
        return user_data