#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
import os, sys

#Database file extension
FILE_EXTENSION_DATABASE = ".db"
#Full directory path that keep this file
THIS_FILE_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))+"\\"
#Directory name to keep the database file
DATABASE_DIRECTORY_NAME = "accountdata"
#Full directory path that keep the database file
DATABASE_DIRECTORY_PATH = THIS_FILE_DIRECTORY_PATH+"\\"+DATABASE_DIRECTORY_NAME+"\\"

def db_create(filename):
    """Create new database file. If already exist database file will return an error."""
    #Convert filename to string and insert file extension for filename
    filename = str(filename)+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist create new one
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        #Change working directory
        os.chdir(THIS_FILE_DIRECTORY_PATH)
        #Make new directory to store the database file
        os.mkdir("accountdata")

    #Check if file already exists, return false and error discription
    if os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return False, "database file already exists"
    
    #Create new database, Change working directory where to store the database file
    os.chdir(DATABASE_DIRECTORY_PATH)
    #Create by connect the database, if not exist it will create the new one
    db_connect = sql.connect(filename)
    #use with to automatically close connection when finish statement (automatic release the resource)
    with db_connect:
        #return true and success discription
        return True, "create new database success"

def db_delete(filename):
    """Delete the database file. If directory or database file not exist will return an error."""
    #Convert filename to string and insert file extension for filename
    filename = str(filename)+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist, return false and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        return False, "no database directory found"

    #Check if file not exist will return False and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return False, "database file not found"

    #Delete database file
    os.remove(DATABASE_DIRECTORY_PATH+filename)
    #return true and success discription
    return True, "delete database successfully"

def db_excecute(filename, sqlscript):
    """____"""
    #Convert filename to string and insert file extension for filename
    filename = str(filename)+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist, return false and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        return False, "no database directory found"

    #Check if file not exist will return False and error message
    if not os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return False, "database file not found"

    #Change working directory
    os.chdir(DATABASE_DIRECTORY_PATH)

    #Try to execute sql script into database, if any error happen rollback the operation
    try:
        #Connect to database
        db_connect = sql.connect(filename)
        db_cursor = db_connect.cursor()

        #Execute the sql script
        db_cursor.executescript(sqlscript)

        #Commit the sql script
        db_connect.commit()

        #return True and success message
        return True, "sql summit complete"
    #Error handling if any error happen
    except sql.Error, e:
        #If connecting the database, Rollback commit script
        if db_connect:
            db_connect.rollback()

        #return False and error message
        return False, "error: %s" % e.args[0]
    #Close connection if program connected to database
    finally:
        if db_connect:
            db_connect.close()

print db_excecute(raw_input(), raw_input())
