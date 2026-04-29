import os
import psycopg
from dotenv import load_dotenv
from psycopg import OperationalError

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

#Creates the weather_info table in PostgreSQL
def create_table():
    connection = None
    cursor = None
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
            
        cursor = connection.cursor()

        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS weather_info(
                        weather_info_id SERIAL PRIMARY KEY,
                        city VARCHAR(100),
                        country VARCHAR(100),
                        latitude DECIMAL(9,6),
                        longitude Decimal(9, 6),
                        temperature Decimal(5,2),
                        windspeed Decimal(5,2),
                        observation_date TIMESTAMP,
                        notes TEXT
                        );
                       """)
        
        connection.commit()
        print("Table for weather_info created successfully")

    except (Exception, psycopg.Error) as error:
        print(f"Error while creating table: {error}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            cursor.close()
            connection.close()

# Inserts a new weatehr observation into the table
def insert_weather(city, country, latitude, longitude, temperature, windspeed,observation_date, notes):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO weather_info (city, country, latitude, longitude, temperature, windspeed, observation_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)RETURNING weather_info_id;
        """
        cursor.execute(insert_query, (city, country, latitude, longitude, temperature, windspeed, observation_date, notes))
        new_id = cursor.fetchone()[0]
        print (f"New record inserted with ID: {new_id}")
        connection.commit()
    
    except(Exception, psycopg.Error) as error:
        print(f"Error while inserting task: {error}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            cursor.close()
            connection.close()
# selects all of the information from the table and returns it
def get_all_observations():
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
            
        cursor = connection.cursor()
            
        select_query = """
        SELECT city, country, latitude, longitude, 
        temperature, windspeed,observation_date, notes
        FROM weather_info
        ORDER By observation_date DESC;
        """
        cursor.execute(select_query)

        observations = cursor.fetchall()
        print(f"Found {len(observations)} observations:")
        for task in observations:
                print(f" - {task[0]}, {task[1]} | Temp: {task[2]} | Humidity: {task[3]} | Date: {task[4]}")

        return observations
            
    except(Exception, psycopg.Error) as error:
        print(f"Error fetching tasks: {error}")
        return []
    
    finally:
        if connection:
            cursor.close()
            connection.close()
#Returns every sing observation matching the give id 
def get_observations_by_id(obs_id):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )

        cursor = connection.cursor()

        select_query = """
        SELECT city, country, latitude, longitude, 
        temperature, windspeed,observation_date, notes
        FROM weather_info
        WHERE weather_info_id = %s
        ORDER By observation_date DESC;
        """
        cursor.execute(select_query, (obs_id,))

        row = cursor.fetchone()
        if row:
            print(f"Found observations: {row}")
        else:
            print(f"No observations found with ID {obs_id}")
        return row
    
    except(Exception, psycopg.Error) as error:
        print(f"Error fetching tasks: {error}")
        return []
    
    finally:
        if connection:
            cursor.close()
            connection.close()
#updates the temperature and humidity for the id thats given
def update_weather(obs_id, notes):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )

        cursor = connection.cursor()

        update_query = """
        UPDATE weather_info
        SET notes = %s
        WHERE weather_info_id = %s;
         """
        cursor.execute(update_query, (notes, obs_id))

        rows_affected = cursor.rowcount

        if rows_affected > 0:
            print(f"Sucessfully were weather updated for ID {obs_id}")
            connection.commit()
        else:
            print(f"There was no record found with ID {obs_id}. update not performed")
    
    except(Exception, psycopg.Error) as error:
        print(f"Error updating task: {error}")
        if connection:
            connection.rollback()
    
    finally:
        if connection:
            cursor.close()
            connection.close()

# Deletes a specific weather observation by its id
def delete_weather(obs_id):
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )

        cursor = connection.cursor()

        delete_query = "DELETE FROM weather_info WHERE weather_info_id = %s; "
        cursor.execute(delete_query, (obs_id,))

        rows_affected = cursor.rowcount

        if rows_affected > 0:
            print(f"Successfully deleted weather id {obs_id}")
            connection.commit()
        else:
            print(f"NO record was found with ID {obs_id}. Nothing was deleted.")

    except (Exception, psycopg.Error) as error:
        print(f"Error deleting task: {error}")
        if connection:
            connection.rollback()
    
    finally:
        if connection:
            cursor.close()
            connection.close()