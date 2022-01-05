import numpy as np
import argparse
import sys
import os
import math

def fread(fid, nelements, dtype):

    """Equivalent to Matlab fread function"""

    if dtype is np.str_:
        dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
    else:
        dt = dtype

    data_array = np.fromfile(fid, dt, nelements)
    data_array.shape = (nelements, 1)

    return data_array

def readRMMD(inputfilename):
    fid = open(inputfilename,'rb')
    fid.seek(0)
    sz = fread(fid,4,'int32').newbyteorder('>');
    data_array = fread(fid,int(sz[1]*sz[2]*sz[3]),'int32').newbyteorder('>')
   
    rmmdData = np.reshape(data_array,(int(sz[3]),int(sz[2]),int(sz[1])),order='F');
    rmmd= np.zeros((int(sz[1]),int(sz[2]),int(sz[3])));
    for k in range(int(sz[1])):
        rmmd[k,:,:] = np.squeeze(rmmdData[:,:,k]).T;
    rmmd = np.flip(rmmd);
    return rmmd

def readCMMI(inputfilename):
    fid = open(inputfilename,'rb')
    fid.seek(0)
    sz = fread(fid,5,np.float32).newbyteorder('>');
    mm = np.zeros((16,int(sz[1]),int(sz[2])))
    for k in range(16):
        fid.seek(0)
        fread(fid,5+k,np.float32).newbyteorder('>');
        mm[k,:,:] = np.reshape(fread(fid, int(sz[1]*sz[2]),np.float32).newbyteorder('>'),(int(sz[1]),int(sz[2])));
    return mm

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
