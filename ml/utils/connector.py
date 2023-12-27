import mysql.connector
import pandas as pd

# Replace these values with your MySQL server credentials
hostname = 'localhost'
username = 'tblex'
password = '1'
database_name = 'recommender'
def connect_to_db(hostname, username, password, database_name):
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database_name
        )

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection
    

def insert_to_movies(connection, df):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"INSERT INTO movies (movieId, title, genres) VALUES (%s, %s, %s)"
            for movieId, title, genres in df.values:
                values = (movieId, title, genres)
                cursor.execute(sql_query, values)
            # Perform database operations here
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def insert_to_ratings(connection, df):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"INSERT INTO ratings (userId, movieId, rating) VALUES (%s, %s, %s)"
            for userId, movieId, rating in df.values:
                values = (userId, movieId, rating)
                cursor.execute(sql_query, values)
            # Perform database operations here
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def get_id(connection, col):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"SELECT DISTINCT {col} FROM ratings;"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            return res
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def check_existence(connection, userId):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"SELECT DISTINCT userId FROM ratings WHERE userId = {userId};"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            if len(res) > 0:
                return True
            else:
                return False
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def get_ratings(connection, userId):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"SELECT userId, movieId, rating FROM ratings WHERE userId = {userId};"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=['userId', 'movieId', 'rating'])
            return df

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def retrieve_movies(connection, col_name, movie_idx):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            if col_name == 'idx':
                indices_str = ', '.join(str(idx + 1) for idx in movie_idx)
            else:
                indices_str = ', '.join(str(idx) for idx in movie_idx)
            sql_query = f"SELECT movieId, title, genres FROM movies WHERE {col_name} IN ({indices_str});"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=['movieId', 'title', 'genres'])
            return df

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

def test(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = f"select * from movies where movieId in (1, 2, 3, 4, 5);"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=['movieId', 'title', 'genres'])
            return df
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Closing the cursor
        if 'cursor' in locals():
            cursor.close()

# conn = connect_to_db(hostname, username, password, database_name)