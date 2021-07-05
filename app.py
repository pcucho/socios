from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL


app = Flask (__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PabloCuchito1974!'
app.config['MYSQL_DATABASE_DB'] = 'socios'

mysql.init_app(app)
@app.route("/")
def index():
    conn = mysql.connect()
    csr = mysql.cursor()
    
    SQL = "insert into socio(nombre, "


    return render_template("socios\index.html")


if __name__ == '__main__':
    app.run(debug=True)

