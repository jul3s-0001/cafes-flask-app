from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'cafes.db'

def get_all_cafes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafe")
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def add_cafe(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cafe (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, 
                          can_take_calls, seats, coffee_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    cafes = get_all_cafes()
    return render_template('index.html', cafes=cafes)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        form = request.form
        data = (
            form['name'], form['map_url'], form['img_url'], form['location'],
            int('has_sockets' in form), int('has_toilet' in form), int('has_wifi' in form),
            int('can_take_calls' in form), form['seats'], form['coffee_price']
        )
        add_cafe(data)
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
