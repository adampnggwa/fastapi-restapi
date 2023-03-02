import mysql.connector
from fastapi import FastAPI

app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

@app.get("/items/")
async def read_items():
    mycursor.execute("SELECT * FROM mytable")
    result = mycursor.fetchall()
    return {"data": result}
