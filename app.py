from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'master#123'
app.config['MYSQL_DB'] = 'users'

# Initialize the MySQL instance
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    port=app.config['MYSQL_PORT'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def get_users_data():
    with mysql.cursor() as cur:
        cur.execute("SELECT * FROM user_info")
        data = cur.fetchall()
    return render_template('users.html', users=data)

@app.route('/create_user', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        with mysql.cursor() as cur:
            cur.execute("INSERT INTO user_info (name, age, city) VALUES (%s, %s, %s)", (name, age, city))
            mysql.commit()

        return redirect(url_for('get_users_data'))

    # Render the form for GET requests
    return render_template('create_user.html')

@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    with mysql.cursor() as cur:
        cur.execute("DELETE FROM user_info WHERE id = %s", (id,))
        mysql.commit()

    return redirect(url_for('get_users_data'))

if __name__ == "__main__":
    app.run(debug=True)
