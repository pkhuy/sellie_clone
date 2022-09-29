from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from models.warehouse.warehouse import warehouse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Product move another file


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
        print("---------------", categories[0].img_url)
        return render_template('index.html', categories=categories)


@app.route('/carts')
def get_cart_detail():
    cart_items = Cart
    return render_template('cart.html', products=products)


@app.route('/categories/<int:id>')
def get_categories_detail(id):
    products = Product.query.all()
    return render_template('product-details.html', products=products)


@app.route('/products')
def get_all_products():
    products = Product.query.all()
    return render_template('product.html', products=products)


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
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('vendor.html')

@app.route('/partners', methods=['POST', 'GET'])
def get_all_partners():
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('partner.html')

@app.route('/customers', methods=['POST', 'GET'])
def get_all_customers():
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('customer.html')


if __name__ == "__main__":
    app.run(debug=True)
