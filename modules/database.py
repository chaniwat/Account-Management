#!usr/bin/python
#-*- encoding: utf-8 -*-

import sqlite3 as sql
import os, md5, time
from mainwindow import FILE_EXTENSION_DATABASE, ROOT_DIRECTORY_PATH, \
                       DATABASE_DIRECTORY_PATH

DATABASE_CHANGE_TYPE_PLUS = ["CHANGE_WALLET_INCOME", "CHANGE_BANK_DEPOSIT", "CHANGE_POT_DEPOSIT", "CHANGE_BANK_TRANSFER_IN"]

class database:
    def __init__(self):
        #Set attribute
        self.connectresult = None
        self.cursor = None
        self.currentaccountid = None

    def connectdatabase(self, filename):
        """Connect to database file"""
        self.connectresult = sql.connect(filename)
        self.cursor = self.connectresult.cursor()

    def closedatabase(self):
        """Close the connection to database

        Result:
            database not connect when try to close the connection: False, 'DB_ERR_NOT_CONNECT'
            close connection success: True, 
        """
        if not self.connectresult:
            return (False, "DB_ERR_NOT_CONNECT")
        else:
            self.connectresult.close()
            return (True, "DB_SUCCESS_CLOSECONNECT")

    def listaccount(self):
        """Return the list of all wallet"""
        #Execute sql script to get the account info (account_info table) of this account and make it as a dict
        self.cursor.execute("SELECT account_id, account_name FROM account_info ORDER BY account_id ASC")
        result = self.cursor.fetchall()

        #Return result
        return True, result

    def addaccount(self, data):
        """add an account for user

        data dict keywords:
        name (account name),
        type (account type), 
        initmoney (start money for this account)
        """
        #account_info table
        self.cursor.execute("INSERT INTO account_info VALUES(NULL, '"+data["name"]+"', '"+data["type"]+"', 'CON', '"+time.strftime("%d-%m-%Y")+"', "+data["initmoney"]+")")
        account_id = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO change_info VALUES(NULL, "+str(self.cursor.lastrowid)+", 'CHANGE_INITIATE', '"+time.strftime("%d-%m-%Y")+"', 'ACCOUNT_INITIATE_TEXT', "+data["initmoney"]+")")
        self.connectresult.commit()       

        return True, account_id

    def deleteaccount(self, account_id):
        """Delete account by id"""
        if account_id == 1:
            print "can't delete this account because this is a main account"
            return False
        else:
            #account_info table
            self.cursor.execute("DELETE FROM account_info WHERE account_id="+str(account_id))
            self.connectresult.commit()
            self.set_currentaccountid()
            return True

    def addrecordtocurrentaccount(self, data):
        """add an record of current account

        data dict keywords:
        type, (type of change)
        description, (description of change)
        amtmoney, (amount of money)
        """
        if data["type"] in DATABASE_CHANGE_TYPE_PLUS:
            self.cursor.execute("SELECT account_currentmoney FROM account_info WHERE account_id="+str(self.get_currentaccountid()))
            newmoney = self.cursor.fetchone()[0]+int(data["amtmoney"])
            self.cursor.execute("UPDATE account_info SET account_currentmoney="+str(newmoney)+" WHERE account_id="+str(self.get_currentaccountid()))
            self.connectresult.commit()
        else:
            self.cursor.execute("SELECT account_currentmoney FROM account_info WHERE account_id="+str(self.get_currentaccountid()))
            newmoney = self.cursor.fetchone()[0]-int(data["amtmoney"])
            if newmoney < 0:
                print "money of this account not have enough money, add some money first"
                return False
            self.cursor.execute("UPDATE account_info SET account_currentmoney="+str(newmoney)+" WHERE account_id="+str(self.get_currentaccountid()))
            self.connectresult.commit()

        self.cursor.execute("INSERT INTO change_info VALUES(NULL, "+str(self.get_currentaccountid())+", '"+data["type"]+"', '"+time.strftime("%d-%m-%Y")+"', '"+data["description"]+"', "+data["amtmoney"]+")")
        self.connectresult.commit()

        return True

    def deleterecord(self, record_id):
        """delete the select record"""
        self.cursor.execute("SELECT change_type FROM change_info WHERE change_id="+str(record_id))
        record_type = self.cursor.fetchone()[0]
        if record_type == "CHANGE_INITIATE":
            print "cannont delete initiate change"
            return False
        elif record_type in DATABASE_CHANGE_TYPE_PLUS:
            self.cursor.execute("SELECT account_currentmoney FROM account_info WHERE account_id="+str(self.get_currentaccountid()))
            currentmoney = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT change_amount FROM change_info WHERE change_id="+str(record_id))
            recordmoney = self.cursor.fetchone()[0]
            newmoney = currentmoney - recordmoney
            if newmoney < 0:
                print "money of this account not have enough money, add some money first"
                return False
            self.cursor.execute("UPDATE account_info SET account_currentmoney="+str(newmoney)+" WHERE account_id="+str(self.get_currentaccountid()))
            self.connectresult.commit()
        else:
            self.cursor.execute("SELECT account_currentmoney FROM account_info WHERE account_id="+str(self.get_currentaccountid()))
            currentmoney = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT change_amount FROM change_info WHERE change_id="+str(record_id))
            recordmoney = self.cursor.fetchone()[0]
            newmoney = currentmoney + recordmoney
            self.cursor.execute("UPDATE account_info SET account_currentmoney="+str(newmoney)+" WHERE account_id="+str(self.get_currentaccountid()))
            self.connectresult.commit()

        self.cursor.execute("DELETE FROM change_info WHERE change_id="+str(record_id))
        self.connectresult.commit()

        return True

    def set_currentaccountid(self, account_id=1):
        """Set the current account to show to user"""
        self.currentaccountid = account_id

    def get_currentaccountid(self):
        """return the current account that show to user"""
        return self.currentaccountid

    def get_currentaccountname(self):
        """return the current account name that show to user"""
        self.cursor.execute("SELECT account_name FROM account_info WHERE account_id = "+str(self.currentaccountid))
        result = self.cursor.fetchone()[0]
        return result

    def get_currentaccounttype(self):
        """return the current account type that show to user"""
        self.cursor.execute("SELECT account_type FROM account_info WHERE account_id = "+str(self.currentaccountid))
        result = self.cursor.fetchone()[0]
        return result

    def get_currentaccountdataall(self):
        """return the change_info of account_id"""
        self.cursor.execute("SELECT change_date, change_type, change_description, change_amount, change_id FROM change_info WHERE account_id = "+str(self.currentaccountid)+" ORDER BY change_id DESC")

        return self.cursor.fetchall()

    def get_currentuserallaccount(self):
        """return all account of current user

        Result:
            True, result

        return result dict keywords:
            account_name,
            account_type,
            account_lastupdate,
            account_currentmoney
        """
        self.cursor.execute("SELECT account_name, account_type, account_lastupdate, account_currentmoney, account_id FROM account_info")

        return self.cursor.fetchall()

    def get_currentuserinfo(self):
        """return the value of current user_info

        Result:
            get user success: True, result

        return result dict keywords:
            USER_NAME,
            USER_SURNAME,
            USER_NICKNAME,
            USER_BIRTHDAY,
            USER_HAS_PWD,
            USER_PWD,
            USER_CREATEDATE,
            USER_LASTEDITDATE
        """
        #Execute sql script to get the account info (user_info table) of this account and make it as a dict
        self.cursor.execute("SELECT * from user_info")
        result = dict(self.cursor.fetchall())

        #Return result
        return True, result

    def get_currentaccountinfo(self):
        """return the info of current account_id"""
        self.cursor.execute("SELECT account_name, account_type, account_lastupdate, account_currentmoney FROM account_info WHERE account_id = "+str(self.currentaccountid))

        return self.cursor.fetchone()

#Normal Function -> use mostly in quick start window
def createnewaccount(data):
    """Create a new account (new database file) to manage a money of person
    data dict keywords:
        name,
        surname,
        nickname,
        birthday (in format: DD-MM-YYYY),
        has_pwd (this account is protected?),
        pwd (if protected, what password?),
        createdate (in format: DD-MM-YYYY), 
        initmoney (start money for this account)

    Result:
        File exist: False, 'DB_ERR_FILE_EXIST'
        Create successful: True, 'DB_SUCCESS_CREATE', filename
    """

    #Create a filename for this account by convert name string to md5
    filename = md5.new(data["name"].encode("utf-8")).hexdigest()+FILE_EXTENSION_DATABASE

    #Check directory to store the database file. if not exist create a new one
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        #Change working directory to root directory
        os.chdir(ROOT_DIRECTORY_PATH)
        #Create new directory
        os.mkdir(DATABASE_DIRECTORY_NAME)

    #Check if file already exists, return an error
    if os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return (False, "DB_ERR_FILE_EXIST")

    #Create new database
    #Change working directory to database directory
    os.chdir(DATABASE_DIRECTORY_PATH)

    #Create tuple of data to insert into new account (user_info table)
    user_info_property = (
        ("USER_NAME", data["name"]),
        ("USER_SURNAME", data["surname"]),
        ("USER_NICKNAME", data["nickname"]),
        ("USER_BIRTHDAY", data["birthday"]),
        ("USER_HAS_PWD", data["has_pwd"]),
        ("USER_PWD", data["pwd"]),
        ("USER_CREATEDATE", data["createdate"]),
        ("USER_LASTEDITDATE", data["createdate"])
    )

    #Create and connect to the database
    db_connect = sql.connect(filename)

    with db_connect:
        db_cursor = db_connect.cursor()

        #Execute sql script to create table and insert data into database
        #user_info table
        db_cursor.execute("CREATE TABLE user_info(property TEXT, vaule TEXT)")
        db_cursor.executemany("INSERT INTO user_info VALUES(?, ?)", user_info_property)
        #account_info table
        db_cursor.execute("CREATE TABLE account_info(account_id INTEGER PRIMARY KEY AUTOINCREMENT, account_name TEXT, account_type TEXT, account_status TEXT, account_lastupdate TEXT, account_currentmoney INTEGER)")
        db_cursor.execute("INSERT INTO account_info VALUES(NULL, 'ACCOUNT_WALLET_NAME', 'ACC_WALLET', 'CON', '"+data["createdate"]+"', "+data["initmoney"]+")")
        #change_info table
        db_cursor.execute("CREATE TABLE change_info(change_id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, change_type TEXT, change_date TEXT, change_description TEXT, change_amount INTEGER)")
        db_cursor.execute("INSERT INTO change_info VALUES(NULL, 1, 'CHANGE_INITIATE', '"+data["createdate"]+"', 'ACCOUNT_INITIATE_TEXT', "+data["initmoney"]+")")

    #return success
    return (True, "DB_SUCCESS_CREATE", filename)

def deleteaccount(filename):
    """Delete an account (database file)

    Result:
        directory not exist: False, 'DB_ERR_DIRECTORY_NOT_FOUND'
        file not exist: False, 'DB_ERR_FILE_NOT_FOUND'
        delete successful: True, 'DB_SUCCESS_DELET'
    """

    #Check database directory, if not exist return an error
    if not os.path.exists(DATABASE_DIRECTORY_PATH):
        return (False, "DB_ERR_DIRECTORY_NOT_FOUND")

    #Check file, if not exist return an error
    if not os.path.exists(DATABASE_DIRECTORY_PATH+filename):
        return (False, "DB_ERR_FILE_NOT_FOUND")

    #Delete database file
    os.remove(DATABASE_DIRECTORY_PATH+filename)
    #return success
    return (True, "DB_SUCCESS_DELETE")

def getuserinfoaccount(filename):
    """return a dict of account info (user_info table)

    Result:
        get user success: True, result

    return result dict keywords:
        USER_NAME,
        USER_SURNAME,
        USER_NICKNAME,
        USER_BIRTHDAY,
        USER_HAS_PWD,
        USER_PWD,
        USER_CREATEDATE,
        USER_LASTEDITDATE
    """
    #Change working directory to database directory
    os.chdir(DATABASE_DIRECTORY_PATH)

    #Connect to database file
    db_connect = sql.connect(filename)

    with db_connect:
        db_cursor = db_connect.cursor()

        #Execute sql script to get the account info (user_info table) of this account and make it as a dict
        db_cursor.execute("SELECT * from user_info")
        result = dict(db_cursor.fetchall())

        #Return result
        return True, result