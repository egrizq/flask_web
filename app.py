from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import os
from flask_session import Session

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

mysql = MySQL(app)

# todo rendering dashboard


@app.route("/")
def home():
    if not session.get("fullname"):
        return redirect("/login")
    return render_template("export.html")

# todo login page


@app.route("/login")
def login():
    return render_template("login.html")

# todo login section


@app.route("/login/form", methods=['POST', 'GET'])
def loginForm():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = 'SELECT fullname FROM data WHERE username = %s AND password = %s'
        cursor = mysql.connection.cursor()
        cursor.execute(query, (username, password))

        # get the fullname data
        result = cursor.fetchone()
        if result:
            # return the fullname from database and store to session
            session['fullname'] = result[0]
        else:
            return render_template("cannot get the data")

        mysql.connection.commit()
        cursor.close()

        return redirect("/")

    return redirect("/login")

# todo logout


@app.route("/logout")
def logout():
    session["fullname"] = None
    return redirect("/login")


# todo register html


@app.route("/register")
def register():
    return render_template("register.html")

# todo register form


@app.route("/register/form", methods=['POST'])
def registerForm():
    if request.method == "POST":
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        queryCheck = 'SELECT username FROM data WHERE username = %s'
        cursor.execute(queryCheck, (username,))
        result = cursor.fetchone()

        if result is not None:
            return render_template("register.html", show_alert=True)
        else:
            queryInsert = 'INSERT INTO data(fullname, username, password) VALUES (%s, %s, %s)'
            cursor.execute(queryInsert, (fullname, username, password))

        mysql.connection.commit()
        cursor.close()
        return render_template("login.html", show_alert=True)


# todo export excel
@app.route("/export", methods=['POST'])
def exportExcel():
    if request.method == 'POST':
        excel = request.files['excel']

        if excel:
            filename = excel.filename
            file_path = os.path.join('static', 'file', filename)
            excel.save(file_path)

    return redirect("/")


if __name__ == '__name__':
    app.run(debug=True)
