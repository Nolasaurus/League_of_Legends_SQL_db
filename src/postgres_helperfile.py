import os
import contextlib
import logging

from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import DatabaseError, IntegrityError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    conn = connect_db()
    with conn.cursor() as cursor:
        # Query to list all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()  # Fetch all table names in the public schema
    print(tables)

class SQLHelper:
    def __init__(self):
        pass

    @contextlib.contextmanager
    def db_connection(self, userrole="readonly"):
        conn = connect_db(userrole)  
        try:
            yield conn
        except psycopg2.DatabaseError as e:
            logging.error("Database error: %s", e)
            conn.rollback()
            raise
        finally:
            conn.close()

    def insert_dict(self, table_name: str, data_dict: dict):
        try:
            with self.db_connection("admin") as conn:
                with conn.cursor() as cursor:
                    columns = ", ".join(data_dict.keys())
                    placeholders = ", ".join(["%s"] * len(data_dict))
                    values = tuple(data_dict.values())

                    insert_stmt = (
                        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    )
                    cursor.execute(insert_stmt, values)
                    conn.commit()
        except Exception as e:
            logging.error("Error in insert_dict: %s", e)
            raise

    def create_read_only_user(self, username, password):
        try:
            with self.db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "CREATE USER %s WITH PASSWORD %s;", (username, password)
                    )
                    cursor.execute(
                        "GRANT CONNECT ON DATABASE loldb TO %s;", (username,)
                    )
                    cursor.execute("GRANT USAGE ON SCHEMA public TO %s;", (username,))
                    cursor.execute(
                        "GRANT SELECT ON ALL TABLES IN SCHEMA public TO %s;",
                        (username,),
                    )
                    cursor.execute(
                        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO %s;",
                        (username,),
                    )
        except Exception as e:
            logging.error("Error in create_read_only_user: %s", e)
            raise

    def execute_query(self, query, values=None, commit=True):
        try:
            with self.db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                    if query.strip().lower().startswith("select"):
                        # Fetch data and column names for SELECT queries
                        rows = cursor.fetchall()
                        columns = [desc[0] for desc in cursor.description]
                        return rows, columns

                    elif commit:
                        # Commit changes for INSERT, UPDATE, DELETE queries
                        conn.commit()

        except Exception as e:
            logging.error("Error in execute_query: %s", e)
            raise


def connect_db(user_role="readonly"):
    # Cloud deployment: DATABASE_URL takes precedence (Neon/Supabase)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url, connect_timeout=10)

    dbname = "loldb"
    user = (
        os.getenv("ADMIN_POSTGRES_USER")
        if user_role == "admin"
        else os.getenv("READONLY_POSTGRES_USER")
    )
    password = (
        os.getenv("ADMIN_POSTGRES_PASSWORD")
        if user_role == "admin"
        else os.getenv("READONLY_POSTGRES_PASSWORD")
    )
    host = "localhost"
    port = "5432"

    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        connect_timeout=10,
    )


def create_postgres_engine():
    # Cloud deployment: DATABASE_URL takes precedence (Neon/Supabase)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return create_engine(database_url)

    dbname = "loldb"
    user = os.getenv("ADMIN_POSTGRES_USER")
    password = os.getenv("ADMIN_POSTGRES_PASSWORD")
    host = "localhost"
    port = "5432"
    connection_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(connection_str)


def execute_sql_file(file_path):
    with open(file_path, "r") as file:
        sql_script = file.read()
        with connect_db("admin") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)


def execute_batch_query(query, values_list, page_size=100):
    """
    Execute a batch SQL query using psycopg2's execute_values method.

    Args:
        query (str): The SQL query template to execute.
        values_list (list of tuple): A list of tuples, each containing the values to insert.
        page_size (int): Number of records to insert in a single batch.

    Returns:
        None
    """
    try:
        with connect_db("admin") as conn:
            with conn.cursor() as cursor:
                # Execute the batch query
                execute_values(cursor, query, values_list, page_size=page_size)
                # Commit the transaction
                conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        raise  # Re-raise the exception to be caught in the calling function


def execute_query(query, data_tuple):
    """
    Execute a single SQL query using psycopg2's execute method.

    Args:
        query (str): The SQL query template to execute.
        data_tuple (tuple): A tuple containing the values to insert.

    Returns:
        None
    """
    try:
        with connect_db("admin") as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data_tuple)
                conn.commit()
                logging.info("Data inserted successfully")

    except IntegrityError as e:
        logging.error("Integrity error occurred: %s", e)
        conn.rollback()  # Rollback in case of error
    except DatabaseError as e:
        logging.error("Database error occurred: %s", e)
        conn.rollback()
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        conn.rollback()


def match_id_not_in_table(table_name, match_id):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                # Ensure table_name is safe to use in the query
                # Example: validate table_name against a list of known table names

                query = f"SELECT match_id FROM {table_name} WHERE match_id = %s"
                cursor.execute(query, [match_id])
                result = cursor.fetchone()  # Fetch one record from the query result
                return result is None  # Return True if no record found

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
import pandas as pd
import psycopg2  # Assuming psycopg2 for PostgreSQL connection
from psycopg2.extensions import AsIs

def df_columns_match_table_columns(cursor, table_name, df):
    cursor.execute("SELECT * FROM %s LIMIT 0", (AsIs(table_name),))
    table_columns = [desc[0] for desc in cursor.description]
    df_columns = df.columns.str.lower().tolist()
    # Compare case-insensitive lists of column names
    return set(df_columns) == set(map(str.lower, table_columns))

def add_df_to_table(table_name, df):
    try:
        with connect_db("admin") as conn:
            with conn.cursor() as cursor:
                if df_columns_match_table_columns(cursor, table_name, df):
                    placeholders = ', '.join(['%s'] * len(df.columns))
                    columns = ', '.join(df.columns)
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    for _, row in df.iterrows():
                        cursor.execute(query, tuple(row))
                    conn.commit()  # Commit the transaction
                    return True
                else:
                    print("DataFrame columns do not match table columns.")
                    return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == '__main__':
    main()