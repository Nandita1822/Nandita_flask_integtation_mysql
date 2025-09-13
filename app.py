from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey" # used for session or message security 

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="company_db"
)
cursor = db.cursor(dictionary=True) #dictionary form me fetch krne ke liye

@app.route("/")
def home():
    return render_template("index.html")

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
(name, email, password))
        db.commit()
        return render_template("index.html", show_signin=True, msg="Signup successful! Please login.")
    except mysql.connector.IntegrityError:
        return render_template("index.html", msg="Already registered. Please login!")

# Signin
@app.route("/signin", methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        session["user"] = user["name"]
        return redirect("/dashboard")
    else:
        return render_template("index.html", show_signin=True, msg="Invalid credentials!")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template("dashboard.html", employees=employees, user=session["user"])

# Add Employee
@app.route("/add_employee", methods=["POST"])
def add_employee():
    if "user" not in session:
        return redirect("/")
    
    name = request.form["name"]
    contact = request.form["contact"]
    position = request.form["position"]
    salary = request.form["salary"]

    cursor.execute("INSERT INTO employees (name, contact, position, salary) VALUES (%s, %s, %s, %s)",
(name, contact, position, salary))
    db.commit()
    return redirect("/dashboard")

# Delete Employee
@app.route("/delete_employee/<int:emp_id>", methods=["POST"])
def delete_employee(emp_id):
    if "user" not in session:
        return redirect("/")
    
    cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
    db.commit()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
