from flask import Flask, render_template, request, jsonify, redirect, url_for, flash 
import pymysql 

app = Flask(__name__)
app.secret_key = 'login'  # Needed for flashing messages

# Database connection settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Default XAMPP MySQL password is empty
DB_NAME = 'cashier'

# Function to create a database connection
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='cashier'
    )
    return connection

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.content_type == 'application/json':
        data = request.get_json()  # Get JSON data
    else:
        data = request.form  # Get form data

    username = data.get('username')
    passcode = data.get('passcode')

    if not username or not passcode:
        flash("Missing 'username' or 'passcode'")
        return redirect(url_for('home'))

    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # Check in manager table
                sql_manager = "SELECT * FROM manager WHERE username=%s AND passcode=%s"
                cursor.execute(sql_manager, (username, passcode))
                manager = cursor.fetchone()

                if manager:
                    return redirect(url_for('manager_dashboard'))

                # Check in users table
                sql_user = "SELECT * FROM users WHERE username=%s AND passcode=%s"
                cursor.execute(sql_user, (username, passcode))
                user = cursor.fetchone()

                if user:
                    return redirect(url_for('dashboard'))

                flash("Invalid credentials")
        finally:
            connection.close()
    else:
        flash("Database connection error")

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('manager.html')

@app.route('/profile')
def profile_management():
    return render_template('profile.html')

@app.route('/inventory_management')
def inventory_management():
    return render_template('inventory.html')

@app.route('/reports_and_sale')
def reports_and_sale():
    return render_template('rep_and_sal.html')

@app.route('/cashier_summary')
def cashier_summary():
    return render_template('cashier_sum.html')


@app.route('/insert', methods=['POST'])
def insert_data():
    if request.content_type == 'application/json':
        data = request.get_json()  # Get JSON data
    else:
        return jsonify({"error": "Invalid content type. Please send data as JSON."}), 400

    name = data.get('name')
    last_name = data.get('last_name')
    username = data.get('username')
    passcode = data.get('passcode')

    if not name or not last_name or not username or not passcode:
        return jsonify({"error": "Missing required fields"}), 400

    # Insert data into MySQL database
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (name, last_name, username, passcode) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, last_name, username, passcode))
                connection.commit()
            return jsonify({"message": "Data inserted successfully"}), 201
        except pymysql.MySQLError as e:
            return jsonify({"error": f"Failed to insert data: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Database connection error"}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users"
                cursor.execute(sql)
                users = cursor.fetchall()
            return jsonify(users)
        except pymysql.MySQLError as e:
            return jsonify({"error": f"Failed to retrieve data: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Database connection error"}), 500

@app.route('/insert_manager', methods=['POST'])
def insert_manager():
    if request.content_type == 'application/json':
        data = request.get_json()  # Get JSON data
    else:
        return jsonify({"error": "Invalid content type. Please send data as JSON."}), 400

    name = data.get('name')
    last_name = data.get('last_name')
    username = data.get('username')
    passcode = data.get('passcode')

    if not name or not last_name or not username or not passcode:
        return jsonify({"error": "Missing required fields"}), 400

    # Insert data into MySQL database
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO manager(name, last_name, username, passcode) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, last_name, username, passcode))
                connection.commit()
            return jsonify({"message": "Manager inserted successfully"}), 201
        except pymysql.MySQLError as e:
            return jsonify({"error": f"Failed to insert data: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Database connection error"}), 500



@app.route('/retrieve_manager', methods=['GET'])
def retrieve_manager():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM manager"
                cursor.execute(sql)
                manager = cursor.fetchall()
            return jsonify(manager)
        except pymysql.MySQLError as e:
            return jsonify({"error": f"Failed to retrieve data: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Database connection error"}), 500
    
    


if __name__ == "__main__":
    app.run(debug=True)