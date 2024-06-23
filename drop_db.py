import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="9069076975"
)

mycursor = mydb.cursor()

sql = "DROP DATABASE paintsite"

mycursor.execute(sql)
print("all done !")
