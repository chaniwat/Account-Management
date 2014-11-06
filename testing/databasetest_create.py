#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
import os, sys

def create_database(db_name):
    #change working directory to current directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    #check folder, if not exist create new one, then change to new directory
    try:
        os.chdir("accountdata")
    except:
        os.mkdir("accountdata")
        os.chdir("accountdata")

    #creating the new database, connect and close new database
    try:
        db_connect = sql.connect(db_name+".db")
        print "Create new database sucessfully."
    except sql.Error, e:
        print "Error: %s" % e.args[0]
        sys.exit(1)
    finally:
        if db_connect:
            db_connect.close()

    #change back to current directory of this file
    os.chdir(current_dir)