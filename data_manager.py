from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from datetime import datetime
datedata = datetime.now().strftime("%Y-%m-%d %H:%M")


@database_common.connection_handler
def get_all_questions(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM question
    ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_by_order(cursor: RealDictCursor, attribute: str, order: str) -> list:
    query = """
    SELECT *
    FROM question
    ORDER BY {} {};
    """.format(attribute, order)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * 
        FROM question
        WHERE id = {};""".format(question_id)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_answer(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT id, message, submission_time, vote_number, image
        FROM answer
        WHERE question_id = {}
        ORDER BY id""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def question_vote_up(cursor: RealDictCursor, question_id : int):
    query = """
    UPDATE question
    SET vote_number =  vote_number + 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def question_vote_down(cursor: RealDictCursor, question_id : int):
    query = """
    UPDATE question
    SET vote_number =  vote_number - 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def answer_vote_up(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = {}""".format(answer_id)
    cursor.execute(query)


@database_common.connection_handler
def answer_vote_down(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = {}""".format(answer_id)
    cursor.execute(query)


@database_common.connection_handler
def add_a_question(cursor, dictionary):
    cursor.execute("""
                    INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                    VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                     """,
                   {'submission_time': datedata,
                    'view_number': dictionary['view_number'],
                    'vote_number': dictionary['vote_number'],
                    'title': dictionary['title'],
                    'message': dictionary['message'],
                    'image': dictionary['image']})


@database_common.connection_handler
def delete_a_question(cursor, question_id):
    cursor.execute("""
                   DELETE FROM answer
                   WHERE question_id = %(question_id)s;
                
                   DELETE FROM question
                   WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})


@database_common.connection_handler
def get_comments(cursor: RealDictCursor, question_id) -> list:
    query = """
    SELECT *
    FROM comment
    where question_id = {}""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT question_id 
        FROM answer
        WHERE id = {}""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchone()




@database_common.connection_handler
def write_question_comment(cursor: RealDictCursor, question_id: int, new_comment: str) -> list:
    query = """
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
    VALUES ({}, NULL ,'{}',CURRENT_TIMESTAMP,0);""".format(question_id, new_comment)
    cursor.execute(query)



@database_common.connection_handler
def update_question(cursor: RealDictCursor, edited_data: dict, question_id: int, image_name:str):
    query = """
        UPDATE question
        SET title=%(title)s, message=%(message)s, image=%(image)s
        WHERE id=%(id)s"""
    var = {'title': edited_data['title'], 'message': edited_data['message'],'image': image_name, 'id': question_id}
    print(image_name)
    cursor.execute(query, var)


@database_common.connection_handler
def add_new_answer(cursor, dictionary):
    cursor.execute("""
                    INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                    VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                    """,
                   {'submission_time': datedata,
                    'vote_number': dictionary['vote_number'],
                    'question_id': dictionary['question_id'],
                    'message': dictionary['message'],
                    'image': dictionary['image']})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                DELETE FROM comment
                WHERE answer_id = %(answer_id)s;
                DELETE FROM answer
                WHERE id = %(answer_id)s;
                """,
                {'answer_id': answer_id})


@database_common.connection_handler
def get_search_results(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT DISTINCT question.id, question.submission_time, question.view_number,
     question.vote_number, question.title, question.message, question.image
    FROM question
    FULL JOIN answer on question.id = answer.question_id
    WHERE answer.message ILIKE %(PHRASE)s
    OR question.message ILIKE %(PHRASE)s 
    OR question.title ILIKE %(PHRASE)s
    """
    var = {'PHRASE': f'%{phrase}%'}
    cursor.execute(query, var)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': answer_id, 'question_id': question_id})
    question_answers_data = cursor.fetchall()
    return question_answers_data


@database_common.connection_handler
def update_answer(cursor, dictionary):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s, image = %(image)s
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': dictionary['id'],
                    'question_id': dictionary['question_id'],
                    'message': dictionary['message'],
                    'image': dictionary['image']})


@database_common.connection_handler
def delete_a_comment(cursor: RealDictCursor, comment_id: int):
    query = """
    DELETE FROM comment
    WHERE id=%(ID)s; 
    """
    var = {'ID': f'{comment_id}'}
    cursor.execute(query, var)


@database_common.connection_handler
def get_image_name_by_answer_id(cursor: RealDictCursor, answer_id: str) -> list:
    query = """
    SELECT image FROM answer
    WHERE id = (%s)"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_image_name_by_question_id(cursor: RealDictCursor, question_id: str) -> list:
    query = """
    SELECT image FROM question
    WHERE id = (%s)"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_all_answers_image_path(cursor: RealDictCursor, question_id: str) -> list:
    query = """
    SELECT id FROM answer
    WHERE question_id = (%s)"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()