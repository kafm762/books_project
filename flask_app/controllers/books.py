from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.user import User
from flask_app.models.comment import Comment

@app.route('/new/book')
def new_book():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_book.html',user=User.get_by_id(data))

@app.route('/create/book',methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect('/new/book')
    data = {
        "title": request.form["title"],
        "author": request.form["author"],
        "genre": request.form["genre"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Book.save(data)
    return redirect('/dashboard')

@app.route('/edit/book/<int:id>')
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_book.html",edit=Book.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/book',methods=['POST'])
def update_book():
    id = request.form['id']
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect(f'/edit/book/{id}')
    data = {
        "title": request.form["title"],
        "author": request.form["author"],
        "genre": request.form["genre"],
        "description": request.form["description"],
        "id":request.form['id']
    }
    Book.update(data)
    return redirect('/dashboard')

@app.route('/book/<int:id>')
def show_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    book_id = {
        "book_id": id
    }
    return render_template("show_book.html",book=Book.get_one(data),user=User.get_by_id(user_data), comments=Comment.get_book_comments(book_id))

@app.route('/destroy/book/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Book.destroy(data)
    return redirect('/dashboard')
    



