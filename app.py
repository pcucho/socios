from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL
from werkzeug.utils import redirect
from datetime import datetime
import os


app = Flask (__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PabloCuchito1974!'
app.config['MYSQL_DATABASE_DB'] = 'socios'
uploads = os.path.join("uploads")
app.config["UPLOADS"] = uploads
mysql.init_app(app)

@app.route("/")
def index():
    conn = mysql.connect()
    csr = conn.cursor()

    SQL = "SELECT * FROM SOCIO"

    csr.execute(SQL)
    socios = csr.fetchall()

    conn.commit()

    return render_template("index.html", socios = socios)

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/store", methods=["POST"])
def store():
    
    _nombre = request.form["txtnombre"]
    _edad = request.form["txtedad"]
    _fecnac = request.form["txtfc"]

    #print(request.files["txtfoto"])
    _foto = request.files["txtfoto"]

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "" :
        _nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save( "Uploads/" + _nuevoNombreFoto )


    sql = "insert into socio (nombre,edad,fecha_nac, foto) values (%s,%s,%s,%s);"

    datos=(_nombre, _edad, _fecnac, _nuevoNombreFoto)
    
    conn = mysql.connect()
    csr = conn.cursor()
    csr.execute(sql,datos)
    conn.commit()

    #return render_template("index.html")
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    sql = "delete from socio where id = %s;"

    conn = mysql.connect()
    csr = conn.cursor()
    csr.execute(sql,id)
    conn.commit()
    return redirect("/")

@app.route("/modify/<int:id>")
def modify(id):
    sql = "Select * from socio where id  = %s;"
    conn = mysql.connect()
    csr = conn.cursor()
    csr.execute(sql,id)
    socios = csr.fetchone()

    conn.commit()

    return redirect("edit.html", socios = socios)

@app.route("/update", methods=['POST'])
def update(id):

    _nombre = request.form["txtnombre"]
    _edad = request.form["txtedad"]
    _fecnac = request.form["txtfc"]
    _id = request.form["txtid"]

    _foto = request.files["txtfoto"]

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "" :
        _nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save( "Uploads/" + _nuevoNombreFoto )

    sql = "Select foto from socio where id  = %s;"
    conn = mysql.connect()
    csr = conn.cursor()
    csr.execute(sql,id)
    nombreFoto = csr.fetchone()[0]

    conn.commit()

    os.remove(os.path.join(app.config["ÜPLOADS"],nombreFoto))

    conn = mysql.connect()
    csr = conn.cursor()
    datos=(_nombre, _edad, _fecnac, _nuevoNombreFoto, id)

    sql = "UPDATE socio SET nombre = %s, edad = %s,fecha_nac = %s , foto = %s where id = $s"
    csr.execute(sql,datos)

    conn.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
