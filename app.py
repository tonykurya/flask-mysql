import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "mydb"
app.config["MYSQL_DATABASE_HOST"] = "mysql.default"
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Flask API!"


@app.route("/create", methods=["POST"])
def add_user():
    """Function to create a user to the MySQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    short_bio = json["short_bio"]
    if name and email and short_bio and request.method == "POST":
        sql = "INSERT INTO users(name, email, short_bio) " \
              "VALUES(%s, %s, %s)"
        data = (name, email, short_bio)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email and short_bio")


@app.route("/users", methods=["GET"])
def users():
    """Function to retrieve all users from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/user/<int:id>", methods=["GET"])
def user(id):
    """Function to get information of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_user():
    """Function to update a user in the MYSQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    short_bio = json["short_bio"]
    id = json["id"]
    if name and email and short_bio and id and request.method == "POST":
        # save edits
        sql = "UPDATE users SET name=%s, email=%s, " \
              "short_bio=%s WHERE id=%s"
        data = (name, email, short_bio, id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("User updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, email and short_bio")


@app.route("/delete/<int:id>")
def delete_user(id):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
