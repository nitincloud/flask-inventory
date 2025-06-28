import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '')
            quantity = int(data.get('quantity', 1))  # Default to 1 if not provided
        else:
            name = request.form.get('name', '')
            quantity = int(request.form.get('quantity', 1))

        if name:
            new_item = Item(name=name, quantity=quantity)
            db.session.add(new_item)
            db.session.commit()

            if request.is_json:
                return jsonify({'message': 'Item added successfully'}), 200
            return redirect('/')
        else:
            return jsonify({'error': 'Missing item name'}), 400

    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='192.168.0.30', port=5000, debug=True)
