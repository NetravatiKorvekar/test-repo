from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="beauty_db"
)
cursor = conn.cursor(dictionary=True)  # Using dictionary cursor globally

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']

        query = "INSERT INTO bookings (name, phone, service, date, time, message) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, phone, service, date, time, message)
        cursor.execute(query, values)
        conn.commit()

        return "Thank you for booking! We'll contact you soon. 💅"
    else:
        return render_template('book.html')

@app.route('/booknow')
def booknow():
    return render_template('booknow.html')

# SINGLE COMBINED DATA ROUTE WITH PAGINATION
@app.route('/data')
def show_data():
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Pagination logic
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM bookings")
        total = cursor.fetchone()['total']
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        # Get paginated data
        offset = (page - 1) * per_page
        cursor.execute("SELECT * FROM bookings LIMIT %s OFFSET %s", (per_page, offset))
        data = cursor.fetchall()
        
        # Close connections
        cursor.close()
        conn.close()
        
        return render_template('data.html', 
                           data=data,
                           page=page,
                           total_pages=total_pages)
        
    except Exception as e:
        return f"Error: {str(e)}", 500
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO bookings (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/data')
@app.route('/test-connection')
def test_conn():
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return "Database connection successful"
    except Exception as e:
        return f"Connection failed: {str(e)}"
if __name__ == '__main__':
    app.run(debug=True)