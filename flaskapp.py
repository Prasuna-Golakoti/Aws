from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for session management

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    # Insert the new user into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, firstname, lastname, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username  # Store the username in the session
            return redirect(url_for('display_user'))
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/display_user')
def display_user():
    username = session.get('username')  # Get the username from the session
    if not username:
        return redirect(url_for('login'))  # If no username in session, redirect to login

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return render_template('display_user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
                                                                                                                                                                                              1,1           Top
