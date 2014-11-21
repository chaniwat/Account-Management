#!usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
import os, sys, md5

#Database file extension
FILE_EXTENSION_DATABASE = ".db"
#Full directory path that keep this file
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))+"\\"
#Directory name to keep the database file
DATABASE_DIRECTORY_NAME = "accountdata"
#Full directory path that keep the database file
DATABASE_DIRECTORY_PATH = THIS_FILE_DIRECTORY_PATH+"\\"+DATABASE_DIRECTORY_NAME+"\\"

def md5_encode(string):
    """return an encode md5 word of string"""
    return md5.new(string).hexdigest()

def createdatabase(data):
    """Create new database file and insert info for user database. If already exist database file will return an error code."""
    #Encode filename to md5 string and insert file extension for filename
    filename = md5_encode(data["name"])+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist create new one
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        #Change working directory
        os.chdir(THIS_FILE_DIRECTORY_PATH)
        #Make new directory to store the database file
        os.mkdir("accountdata")

    #Check if file already exists, return false and error code
    if os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return False, "DB_ERR_FILE_EXIST"
    
    #Create new database, Change working directory where to store the database file
    os.chdir(DATABASE_DIRECTORY_PATH)

    #Create tuple of property data to insert into database user_info table
    user_info_property = (
        ("USER_NAME", "'"+data["name"].decode(sys.stdin.encoding)+"'"),
        ("USER_SURNAME", "'"+data["surname"].decode(sys.stdin.encoding)+"'"),
        ("USER_NICKNAME", "'"+data["nickname"].decode(sys.stdin.encoding)+"'"),
        ("USER_BIRTHDATE", "'"+data["birthday"].decode(sys.stdin.encoding)+"'"),
        ("USER_HAS_PWD", data["has_pwd"].decode(sys.stdin.encoding)),
        ("USER_PWD", data["pwd"].decode(sys.stdin.encoding)),
        ("USER_CREATE_DATE", data["create_date"].decode(sys.stdin.encoding)),
        ("USER_LASTEDIT_DATE", data["lastedit_date"].decode(sys.stdin.encoding))
    )

    #Create by connect the database, if not exist it will create the new one
    db_connect = sql.connect(filename)

    #use with to automatically close connection when finish statement (automatic release the resource)
    with db_connect:
        #Cursor the connection
        db_cursor = db_connect.cursor()
        
        #Execute sql script to create table and insert data into database
        #Create user_info table and insert property data
        db_cursor.execute("CREATE TABLE user_info(property TEXT, value TEXT)")
        db_cursor.executemany("INSERT INTO user_info VALUES(?, ?)", user_info_property)
        #Create account_info table and add first account
        db_cursor.execute("CREATE TABLE account_info(account_id INTEGER PRIMARY KEY AUTOINCREMENT, account_name TEXT, account_type TEXT, account_status TEXT, account_lastupdate TEXT)")
        db_cursor.execute("INSERT INTO account_info VALUES(NULL, 'wallet', 'ACC_WALLET', 'CON', '"+data["create_date"].decode(sys.stdin.encoding)+"')")
        #Create change_info table and add first money change
        db_cursor.execute("CREATE TABLE change_info(change_id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, change_type TEXT, change_date TEXT, change_description TEXT, change_amount INTEGER)")
        db_cursor.execute("INSERT INTO change_info VALUES(NULL, 1, 'CHANGE_INITIATE', '"+data["create_date"].decode(sys.stdin.encoding)+"', '', "+data["money"].decode(sys.stdin.encoding)+")")

    #return true and success code
    return True, "DB_SUCCESS_CREATE"

def deletedatabase(filename):
    """Delete the database file. If directory or database file not exist will return an error code."""
    #Convert filename to string and insert file extension for filename
    filename = filename+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist, return false and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        return False, "DB_ERR_DIRECTORY_NOT_FOUND"

    #Check if file not exist will return False and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return False, "DB_ERR_FILE_NOT_FOUND"

    #Delete database file
    os.remove(DATABASE_DIRECTORY_PATH+filename)
    #return true and success discription
    return True, "DB_SUCCESS_DELETE"

def listdatabase():
    """return the data of each database that created, if no database found will return an error code"""
    #Check directory to store the database file. if not exist, return false and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        return False, "DB_ERR_DIRECTORY_NOT_FOUND"

    #Change working directory to where that store the database file
    os.chdir(DATABASE_DIRECTORY_PATH)

    #List file that contain in directory
    file_list = os.listdir(os.getcwd())
    #Filter the .db files
    file_db_list = filter(lambda x: x[-1:-4:-1][::-1] == FILE_EXTENSION_DATABASE, file_list)

    #Create the variable to store the result
    result = list()

if __name__ == "__main__":
    print createdatabase(input())