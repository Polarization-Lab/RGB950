
import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_server_connection(host_name, user_name, user_password):
    """Establish a connection to a mySQL server
        Parameters
        ----------
        host_name : str
        user_name : str
        user_password : str
            
        Returns
        -------
        connection : connection object 
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    """Establish a connection to a mySQL server
        Parameters
        ----------
        connection : connection object
        query : a SQL query
        
    """
    
    cursor = connection.cursor()
    try:
        cursor.execute(query,{'sample_no': sample_no, 
             'date': date, 
             'wavelength': wavelength, 
             'exposure': exposure,
             'AOI': AOI,
             'AOC': AOC,
             'f_no':f_no})
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        
def create_db_connection(host_name, user_name, user_password, db_name):
    
    """Establish a connection to a mySQL server
        Parameters
        ----------
        host_name : str
        user_name : str
        user_password : str
        db_name : str
            
        Returns
        -------
        connection : connection object 
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
                auth_plugin = 'mysql_native_password'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

        
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        