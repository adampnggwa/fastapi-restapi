from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import mysql.connector
from fastapi.responses import JSONResponse

app = FastAPI(title="Server Adam Punggawa")

# model input
class DataModel(BaseModel):
    nama: str
    hobi: str

# koneksi ke database mysql
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="datauser"
)

#untuk mengetahui ip dan user web browser 
def headers(request: Request):
    pengguna = request.headers.get("user-agent")
    ip = request.headers.get("x-forwarded-for")
    if pengguna is None:
        pengguna = "data tidak ditemukan"
    if ip is None:
        ip = "ip tidak ditemukan"    
    return{"user": pengguna, "IP": ip}

# membuat objek cursor
cursor = db.cursor()

# method get untuk menampilkan semua data
@app.get("/user/", tags=["Read Data"], summary="Menampilkan Data")
async def tampilkan(request: Request):
    cursor.execute("SELECT * FROM siswa")
    atas = headers(request)
    results = cursor.fetchall()
    return JSONResponse(content={"message": "data berhasil ditampilkan", "results": results}, headers=atas)

# method get untuk mencari data berdasarkan ID
@app.get("/user/{id}", tags=["Read Data"], summary="Mencari Data")
async def cari(id: int, request: Request):
    cursor.execute("SELECT * FROM siswa WHERE id = %s", (id,))
    atas = headers(request)
    results = cursor.fetchone()
    return JSONResponse(content={"message": "data berhasil ditemukan", "result": results}, headers=atas)

# method post untuk menambahkan data
@app.post("/user/", tags=["Create Data"], summary="Menambah Data")
async def tambah(data: DataModel, request: Request):
    cursor.execute("INSERT INTO siswa (nama, hobi) VALUES (%s, %s)", (data.nama, data.hobi))
    atas = headers(request)
    db.commit()
    return JSONResponse(content={"message": "data berhasil ditambahkan"}, headers=atas)

# method delete untuk menghapus data berdasarkan ID
@app.delete("/user/{id}", tags=["Delete Data"], summary="Menghapus Data")
async def hapus(id: int, request: Request):
    cursor.execute("DELETE FROM siswa WHERE id = %s", (id,))
    atas = headers(request)
    db.commit()
    return JSONResponse(content={"massage": "data berhasil dihapus"}, headers=atas)

# method patch untuk memperbarui data yang diinginkan
@app.patch("/user/{id}", tags=["Update Data"], summary="Memperbarui Data")
async def update(id: int, data: DataModel, request: Request):
    query = "UPDATE siswa SET "
    values = []
    if data.nama:
        query += "nama=%s, "
        values.append(data.nama)
    if data.hobi:
        query += "hobi=%s, "
        values.append(data.hobi)
    query = query[:-2]
    query += " WHERE id=%s"
    values.append(id)
    cursor.execute(query, tuple(values))
    atas = headers(request)
    db.commit()
    return JSONResponse(content={"message": "data berhasil diperbarui"}, headers=atas)
    
# method put untuk memperbarui seluruh data
@app.put("/user/{id}", tags=["Update Data"], summary="Memperbarui Seluruh Data")
async def update_all(id: int, data: DataModel, request: Request):
    cursor.execute("UPDATE siswa SET nama = %s, hobi = %s WHERE id = %s",
    (data.nama, data.hobi, id))
    atas = headers(request)
    db.commit()
    return JSONResponse(content={"massage": "data berhasil di update"}, headers=atas)

#detail keselahan
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_msg = f"Error occurred: {str(exc)}"
    return JSONResponse(status_code=500, content={"message": error_msg})   
