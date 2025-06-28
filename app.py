# app.py
import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

# Ensure the database is created in the same folder as app.py
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            quantity = data.get('quantity')
        else:
            name = request.form['name']
            quantity = request.form['quantity']

        new_item = Item(name=name, quantity=int(quantity))
        db.session.add(new_item)
        db.session.commit()

        if request.is_json:
            return jsonify({'message': 'Item added successfully'}), 200

        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='192.168.0.30', port=5000, debug=True)
