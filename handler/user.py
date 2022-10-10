from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user

import service
user_api = Blueprint("user_api", __name__)




@user_api.route('/<string:role>', methods=['POST', 'GET'])
def get_users(role):
    if request.method == 'POST':
        return render_template('dashboard.html')
    else:
        # customer role id = 2
        # partner role id = 3
        # vendor role id = 4
        if role == 'customer':
            res = service.User.get_users(2)
            render_template()
        if role == 'partner':
            res = service.User.get_users(3)
        if role == 'vendor':
            res = service.User.get_users(4)
        users = service.User.get_users()
        return render_template('users.html', context=users)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
