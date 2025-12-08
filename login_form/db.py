import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",      
        password="Rupali09",      
        database="userdb"
    )
