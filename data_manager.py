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