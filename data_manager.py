from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from datetime import datetime
datedata = datetime.now().strftime("%Y-%m-%d %H:%M")


@database_common.connection_handler
def get_last_5(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


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
def get_answer_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT id, message, submission_time, vote_number, image, accepted, user_id
        FROM answer
        WHERE question_id = {}
        ORDER BY id""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT *
        FROM answer
        WHERE id = {}""".format(answer_id)
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
                    INSERT INTO question(submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s,
                     %(user_id)s);
                     """,
                   {'submission_time': datedata,
                    'view_number': dictionary['view_number'],
                    'vote_number': dictionary['vote_number'],
                    'title': dictionary['title'],
                    'message': dictionary['message'],
                    'image': dictionary['image'],
                    'user_id': dictionary['user_id']})


@database_common.connection_handler
def delete_a_question(cursor, question_id):
    cursor.execute("""
                           DELETE FROM question_tag
                           WHERE question_id = %(question_id)s;
                           """,
                   {'question_id': question_id})

    cursor.execute("""
                       DELETE FROM comment
                       WHERE question_id = %(question_id)s;
                       """,
                   {'question_id': question_id})

    cursor.execute("""
                       DELETE FROM comment
                       WHERE EXISTS(
                       SELECT comment.* 
                       FROM comment, answer
                       WHERE comment.answer_id = answer.id 
                       AND answer.question_id = %(question_id)s
                               );
                       """,
                   {'question_id': question_id})

    cursor.execute("""
                       DELETE FROM answer
                       WHERE question_id = %(question_id)s;
                       """,
                   {'question_id': question_id})

    cursor.execute("""
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
def get_question_id_from_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT question_id 
        FROM answer
        WHERE id = {}""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def write_question_comment(cursor: RealDictCursor, question_id: int, new_comment: str, user_id: int) -> list:
    query = """
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
    VALUES ({}, NULL ,'{}',CURRENT_TIMESTAMP,0, {});""".format(question_id, new_comment, user_id)
    cursor.execute(query)


@database_common.connection_handler
def update_question(cursor: RealDictCursor, edited_data: dict, question_id: int, image_name:str):
    query = """
        UPDATE question
        SET title=%(title)s, message=%(message)s, image=%(image)s
        WHERE id=%(id)s"""
    var = {'title': edited_data['title'], 'message': edited_data['message'],'image': image_name, 'id': question_id}
    cursor.execute(query, var)


@database_common.connection_handler
def add_new_answer(cursor, dictionary):
    cursor.execute("""
                    INSERT INTO answer(submission_time, vote_number, question_id, message, image, accepted, user_id)
                    VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(accepted)s, %(user_id)s);
                    """,
                   {'submission_time': datedata,
                    'vote_number': dictionary['vote_number'],
                    'question_id': dictionary['question_id'],
                    'message': dictionary['message'],
                    'image': dictionary['image'],
                    'accepted': dictionary['accepted'],
                    'user_id': dictionary['user_id']})


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
def get_question_by_phrase(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT DISTINCT question.id, question.submission_time, question.view_number,
     question.vote_number, question.title, question.message, question.image
    FROM question
    LEFT JOIN answer on question.id = answer.question_id
    WHERE answer.message ILIKE %(PHRASE)s
    OR question.message ILIKE %(PHRASE)s 
    OR question.title ILIKE %(PHRASE)s
    """
    var = {'PHRASE': f'%{phrase}%'}
    cursor.execute(query, var)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_phrase(cursor: RealDictCursor, phrase: str) -> list:
    query = """
    SELECT DISTINCT question.id, question.title, answer.message
    FROM question
    LEFT JOIN answer on question.id = answer.question_id
    WHERE answer.message ILIKE %(PHRASE)s
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


@database_common.connection_handler
def increase_view_number(cursor: RealDictCursor, question_id: str) -> list:
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = (%s)"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def write_answer_comment(cursor: RealDictCursor, answer_id: int, new_comment: str, user_id: int) -> list:
    query = """
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
    VALUES (NULl, {} ,'{}',CURRENT_TIMESTAMP,0,{});""".format(answer_id, new_comment, user_id)
    cursor.execute(query)


@database_common.connection_handler
def get_question_comments(cursor: RealDictCursor, question_id:int):
    query = """
    SELECT *
    FROM comment
    WHERE question_id = {};""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_comments(cursor: RealDictCursor, answer_id:int):
    query = """
    SELECT * 
    FROM comment
    WHERE answer_id = {};""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_data(cursor: RealDictCursor, username:str, password:int):
    query = """
        SELECT id, username, 
        CONVERT_FROM(password, 'UTF8') AS password
        FROM users
        WHERE username= %(username)s"""
    cursor.execute(query, {'username': username,})
    return cursor.fetchone()


@database_common.connection_handler
def show_tags(cursor, question_id):
    cursor.execute("""
                    SELECT tag.* 
                    FROM tag, question_tag
                    WHERE tag.id = question_tag.tag_id 
                    AND question_tag.question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question_tags = cursor.fetchall()
    return question_tags


@database_common.connection_handler
def add_new_tag(cursor, dictionary, question_id):
    cursor.execute("""
                    INSERT INTO tag(name)
                    VALUES (%(name)s);
                    """,
                   {'name': dictionary})

    cursor.execute("""
                    SELECT id 
                    FROM tag
                    WHERE name = %(name)s;
                    """,
                   {'name': dictionary})
    tag_id_dict = cursor.fetchone()
    tag_id = tag_id_dict['id']

    cursor.execute("""
                    INSERT INTO question_tag(question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s);
                    """,
                   {'question_id': question_id,
                    'tag_id': tag_id})


@database_common.connection_handler
def add_new_user(cursor: RealDictCursor, username, password, registration_date, count_of_asked_questions, count_of_answers, count_of_comments, reputation):
    query = """
    INSERT INTO users (username, password, registration_date, count_of_asked_questions,
    count_of_answers, count_of_comments, reputation)
    VALUES (%(username)s, %(password)s, %(registration_date)s, 
    %(count_of_asked_questions)s, %(count_of_answers)s, %(count_of_comments)s, %(reputation)s)"""
    cursor.execute(query, {'username': username, 'password': password, 'registration_date': registration_date, 'count_of_asked_questions': count_of_asked_questions,
    'count_of_answers': count_of_answers, 'count_of_comments': count_of_comments, 'reputation': reputation},)

# @database_common.connection_handler
# def add_new_user(cursor: RealDictCursor, username, password, registration_date):
#     query = """
#     INSERT INTO users (username, password, registration_date)
#     VALUES (%(username)s, %(password)s, %(registration_date)s)"""
#     cursor.execute(query, {'username': username, 'password': password, 'registration_date': registration_date},)


@database_common.connection_handler
def delete_tag(cursor, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE tag_id = %(tag_id)s;
                    """,
                   {'tag_id': tag_id})

    cursor.execute("""
                    DELETE FROM tag
                    WHERE id = %(tag_id)s;
                    """,
                   {'tag_id': tag_id})


@database_common.connection_handler
def get_all_users(cursor: RealDictCursor) -> list:
    query = """
        SELECT username, registration_date, count_of_asked_questions, count_of_answers, count_of_comments, reputation
        FROM users
        ORDER BY username ASC"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id(cursor: RealDictCursor, username: str):
    query = """
        SELECT id
        FROM users
        WHERE username = %(usr)s"""
    usr = {'usr': username}
    cursor.execute(query, usr)
    return cursor.fetchone()


@database_common.connection_handler
def get_user_details(cursor: RealDictCursor, user_id: str):
    query = """
        SELECT id, username, registration_date, count_of_asked_questions,
         count_of_answers, count_of_comments, reputation
        FROM users
        WHERE id = %(usr_id)s"""
    usr_id = {'usr_id': user_id}
    cursor.execute(query, usr_id)
    return cursor.fetchone()

@database_common.connection_handler
def get_user_questions(cursor: RealDictCursor, user_id: str):
    query = """
        SELECT id, title, message
        FROM question
        WHERE question.user_id = %(usr_id)s"""
    usr_id = {'usr_id': user_id}
    cursor.execute(query, usr_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_user_answers(cursor: RealDictCursor, user_id: str):
    query = """
        SELECT question.id as question_id, question.title as title, question.message as question_message,
         answer.message as answer_message, answer.id as answer_id
        FROM question
        INNER JOIN answer ON answer.question_id = question.id
        WHERE question.user_id = %(usr_id)s"""
    usr_id = {'usr_id': user_id}
    cursor.execute(query, usr_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_comments_for_question(cursor: RealDictCursor, user_id: str):
    query = """
        SELECT question.id as question_id, question.title as title,
         comment.message as comment_message
        FROM question
        INNER JOIN comment ON comment.question_id = question.id
        WHERE comment.user_id = %(usr_id)s;
        """
    usr_id = {'usr_id': user_id}
    cursor.execute(query, usr_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment_for_answer(cursor: RealDictCursor, user_id: str):
    query = """
        SELECT DISTINCT comment.message as comment_message, answer.question_id as question_id, answer.id as answer_id
        FROM comment
        LEFT JOIN answer ON comment.user_id = answer.user_id 
        WHERE comment.user_id = %(user_id)s and answer.id = comment.answer_id;
        """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()



@database_common.connection_handler
def get_status_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """
    SELECT accepted
    FROM answer
    WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id, })
    return cursor.fetchone()


@database_common.connection_handler
def set_status_by_answer_id(cursor, answer_id, status):
    query = """
    UPDATE answer
    SET accepted = %(status)s
    WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id, 'status': status})


@database_common.connection_handler
def update_comments(cursor: RealDictCursor, updated_comment:dict):
    query = """ 
            UPDATE comment
            SET message = %(message)s,
            submission_time = %(submission_time)s
            WHERE id = %(id)s
        """
    value = {'message' : updated_comment["message"], "id": updated_comment["id"], "submission_time": updated_comment["submission_time"]}
    cursor.execute(query, value)


@database_common.connection_handler
def get_comment_by_id(cursor : RealDictCursor, id: int):
    query = """
            SELECT *
            FROM comment
            WHERE id = %(id)s
            """
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def increase_edit_number(cursor: RealDictCursor, comment_id):
    query = """
            UPDATE comment
            SET edited_count = edited_count + 1
            WHERE id = (%s)
    """
    cursor.execute(query, (comment_id,))


@database_common.connection_handler
def get_question_id_from_comment(cursor: RealDictCursor, comment_id) -> list:
    query = """
        SELECT question_id 
        FROM comment
        WHERE id = {}""".format(comment_id)
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_question_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT question_id 
        FROM answer
        WHERE id = {}""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def reputation_up(cursor: RealDictCursor, user_id: int, value:int):
    query = """
    UPDATE users
    SET reputation = reputation + %(value)s
    WHERE id = %(user_id)s
    """
    dict = {"user_id": user_id, "value": value}
    cursor.execute(query, dict)


@database_common.connection_handler
def reputation_down(cursor: RealDictCursor, user_id: int, value:int):
    query = """
    UPDATE users
    SET reputation = reputation - %(value)s
    WHERE id = %(user_id)s
    """
    dict = {"user_id": user_id, "value": value}
    cursor.execute(query, dict)#


@database_common.connection_handler
def get_user_id(cursor: RealDictCursor, username: str):
    query = """
        SELECT id
        FROM users
        WHERE username = %(usr)s"""
    usr = {'usr': username}
    cursor.execute(query, usr)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id:int):
    query = """
    SELECT *
    FROM question
    WHERE id = %(id)s
    """
    value ={"id": id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_comment_id(cursor: RealDictCursor, id:int):
    query = """
    SELECT *
    FROM answer
    WHERE id = %(id)s
    """
    value ={"id": id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                    SELECT name, 
                    COUNT(question_id) AS Number_of_Questions
                    FROM tag 
                    JOIN question_tag ON tag.id = question_tag.tag_id
                    GROUP BY name;
                    """)
    all_tags = cursor.fetchall()
    return all_tags


# @database_common.connection_handler
# def check_user_id_by_question_id(cursor: RealDictCursor, user_id: str):
#     query = """
#     SELECT id
#     FROM answer
#     WHERE user_id = %(user_id)s;"""
#     cursor.execute(query, {'user_id': user_id, })
#     return cursor.fetchall()


@database_common.connection_handler
def validate_user_by_answer_id(cursor: RealDictCursor, answer_id: str):
    query = """
    SELECT user_id
    FROM answer
    WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id, })
    return cursor.fetchone()
