import mysql.connector
from mysql.connector import Error

class Config:
    rootSampleDirectory = ""
    hostName = ""
    userName  = ""
    userPassword= ""
    dbName = ""

def createDBConnection(hostName, userName, userPassword, dbName):
    
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
    # try:
    connection = mysql.connector.connect(
        host=hostName,
        user=userName,
        passwd=userPassword,
        database=dbName,
        auth_plugin = 'mysql_native_password'
        )
        #print("MySQL Database connection successful")
    # except Error as err:
    #    print(f"Error: '{err}'")

    return connection

def readQuery(connection, query, data):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, data)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
