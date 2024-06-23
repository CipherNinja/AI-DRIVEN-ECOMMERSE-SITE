from mysql.connector import connect

database = connect(
    host="localhost",
    user="root",
    passwd="9069076975"
)

cursor_object = database.cursor()
cursor_object.execute("CREATE DATABASE paintsite01")

print("ALL DONE !")