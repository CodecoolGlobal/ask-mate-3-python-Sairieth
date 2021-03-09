from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from datetime import datetime
datedata = datetime.now().strftime("%Y-%m-%d %H:%M")


# @database_common.connection_handler
# def valami_funkció(cursor: RealDictCursor) -> list:
#     query = """
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


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
