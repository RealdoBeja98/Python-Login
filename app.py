from flask import  Flask, render_template, redirect
from flask import request, logging, url_for, session, flash
import  sqlite3
from passlib.hash import sha256_crypt
app =Flask(__name__)

#connect to database
conn = sqlite3.connect('register.db', check_same_thread = False)
#create the cursor
cursor = conn.cursor()

#create the table users
sql = '''CREATE TABLE IF NOT EXISTS Users
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name VARCHAR(50),
          username VARCHAR(50),
          password VARCHAR(300))'''

cursor.execute(sql)


@app.route("/")
def home():
    return render_template("home.html")

#register form
@app.route("/register", methods=["GET", "POST"])
def register():
    #here in this part you take all of the information from the inside labels of register form
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm_password:
            sql = "INSERT INTO Users (name, username, password) VALUES ('{}','{}','{}')".format(name, username, secure_password)
            cursor.execute(sql)
            conn.commit()
            flash("You are now registered and now you can login", "success")
            return redirect(url_for('home'))
        else:
            flash("PASSWORD does not match", "danger")
            return render_template("register.html")
    return render_template("register.html")

#login form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_request_taken = request.form.get("username")
        password_request_taken = request.form.get("passqord")
        cursor.execute("SELECT username FROM Users WHERE username=? ", (username_request_taken,))
        username_fetched =  cursor.fetchone()
        cursor.execute("SELECT password FROM Users WHERE username=?", (username_request_taken,))
        password_fetched = cursor.fetchone()

        if username_fetched is None:
            flash("Username does not exists", "danger")
            return render_template("login.html")
        else:
            for password in password_fetched:
                if sha256_crypt.verify(password_request_taken, password):
                    flash("You are now login", "success")
                    return redirect(url_for('photo'))
                else:
                    flash("Incorrect password", "danger")
                    return render_template("login.html")
    return render_template("login.html")



if __name__ == '__main__':
    app.secret_key = "13d2946b5197431ebe2cd714529a8baa"
    app.run(debug = True)


conn.close()