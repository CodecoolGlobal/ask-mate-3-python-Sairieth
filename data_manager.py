from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

datedata = datetime.now().strftime("%Y-%m-%d %H:%M")
import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor ) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM question
    ORDER BY submission_time DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_questions_by_order(cursor: RealDictCursor, attribute: str, order: str) -> list:
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
        SELECT id, message, submission_time, vote_number
        FROM answer
        WHERE question_id = {}
        ORDER BY id""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def vote_up(cursor: RealDictCursor, question_id : int):
    query = """
    UPDATE question
    SET vote_number =  vote_number + 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def vote_down(cursor: RealDictCursor, question_id : int):
    query = """
    UPDATE question
    SET vote_number =  vote_number - 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)