from unicodedata import category
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from models.warehouse.warehouse import warehouse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Product move another file


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200))



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    cart_id = db.Column(db.Integer)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Product(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        categories = Category.query.order_by(Category.id).all()
        return render_template('index.html', categories=categories)


@app.route('/products')
def get_products():
    products = Product.query.all()
    products = [{
        "id": 1,
        "name": "Piano",
        "img_url": "",
        "price": "$2000",
        "description": "Some description",
    }, {
        "id": 1,
        "name": "Violin",
        "img_url": "",
        "price": "$2000",
        "description": "Some description",
    }, {
        "id": 1,
        "name": "Organ",
        "img_url": "",
        "price": "$2000",
        "description": "Some description",
    }, {
        "id": 1,
        "name": "Ukulele",
        "img_url": "",
        "price": "$2000",
        "description": "Some description",
    }, {
        "id": 1,
        "name": "Lyre",
        "img_url": "",
        "price": "$2000",
        "description": "Some description",
    }]
    categories = Category.query.order_by(Category.id).all()
    category = categories[3]
    return render_template('product.html', products=products, category=category)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Product.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/vendors', methods=['POST', 'GET'])
def get_all_vendors():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Product(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Product.query.order_by(Product.date_created).all()
        return render_template('vendor.html', tasks=tasks, warehouse=warehouse)

if __name__ == "__main__":
    app.run(debug=True)
