import mysql.connector
from fastapi import FastAPI

app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="datauser"
)

mycursor = mydb.cursor()

@app.get("/items/")
async def read_items():
    mycursor.execute("SELECT * FROM siswa")
    result = mycursor.fetchall()
    return {"data": result}
