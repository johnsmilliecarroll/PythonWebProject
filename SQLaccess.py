# https://realpython.com/python-sql-libraries/
import mysql.connector
from mysql.connector import Error

# credentials needed for the sql connection
hostname = "localhost"
myusername = "root"
mypassword = "password01"  # make sure to set this to your root password
db = "accountsdatabase"


def createDB():  # creates the database if it doesn't exist yet.
    newdb = mysql.connector.connect(host=hostname, username=myusername, password=mypassword)
    cursor = newdb.cursor()
    cursor.execute("SHOW DATABASES")  # check all databases
    dbexists = False
    for x in cursor:
        if str(x) == "('accountsdatabase',)":  # if a db equals this, it exists
            dbexists = True
    if not dbexists:  # if the database doesnt exist, create it!
        try:
            cursor.execute('CREATE DATABASE accountsdatabase;')
            cursor.execute('CREATE TABLE accountsdatabase.accounts (userid int NOT NULL AUTO_INCREMENT, '
                           'username VARCHAR(45) DEFAULT NULL, '
                           'password VARCHAR(45) DEFAULT NULL, '
                           'email VARCHAR(45) DEFAULT NULL, PRIMARY KEY (userid)) '
                           'ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;')
        except Error as e:  # if theres an error catch it and print it
            print("ERROR: " + str(e))


def connectToDB():  # returns a connection to the database using the credentials at the top of the program
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            username=myusername,
            password=mypassword,
            database=db
        )
        print("We have connected to " + db + " successfully!")
    except Error as e:
        print("ERROR: " + str(e))
    return connection


def validateLogin(connection, username, password):  # returns true if the username with that password is in the database
    success = False
    cursor = connection.cursor(buffered=True)  # create a buffered cursor based off the connection
    try:
        data = (username, password)  # use SQL parameters instead of string concatenation to prevent injection
        cursor.execute("SELECT * from Accounts where username = %s and password = %s;", data)
        connection.commit()  # confirm changes
        result = cursor.fetchall()  # gets the result of the query
        print("The Query was executed successfully.")
        if str(result) != "[]":  # if there were results, then set the bool to true
            success = True
    except Error as e:
        print("ERROR: " + str(e))
    return success


def registerUser(connection, email, username, password):  # inserts an entry into the accounts database
    success = False
    cursor = connection.cursor(buffered=True)
    try:
        data = (email, username, password)  # use SQL parameters instead of string concatenation to prevent injection
        cursor.execute("INSERT into Accounts (email, username, password) values (%s,  %s , %s)", data)
        connection.commit()
        print(str(username) + " was put entered the database successfully.")
        success = True
    except Error as e:
        print("ERROR: " + str(e))
    return success
