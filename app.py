from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# MYSQL CONNECTION
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agendavirtual'
db = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM contact')
    data = cur.fetchall()

    return render_template('index.html', contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        note = request.form['nota']

    cur = db.connection.cursor()
    cur.execute('INSERT INTO contact (fullname, phone, email, nota) VALUES (%s, %s, %s, %s)',(fullname, phone, email, note))
    db.connection.commit()
    flash("Contact added succesfully")
    
    return redirect(url_for('Index'))


@app.route('/edit/<id>')
def get_contact(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM contact WHERE id = %s', (id))
    data = cur.fetchall()


    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        note = request.form['nota']

    cur = db.connection.cursor()
    cur.execute('UPDATE contact SET fullname = %s, phone = %s, email = %s, nota = %s WHERE id = %s', (fullname, phone, email, note, id))
    db.connection.commit()

    flash('Contact updated successfully')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM contact WHERE id = {0}'.format(id))
    db.connection.commit()
    flash('Contact removed Successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 80, debug=True)  # Puerto +  debug (actualiza en tiempo real)