from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def valami_funkció(cursor: RealDictCursor) -> list:
    query = """
    """
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