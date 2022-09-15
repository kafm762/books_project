from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.comment import Comment
from flask_app.models.book import Book
from flask_app.models.user import User

@app.route('/new/<int:book_id>/comment')
def new_comment(book_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    } 
    data = {
        "id": book_id
    }
    return render_template('new_comment.html',books=Book.get_one(data), user=User.get_by_id(user_data))


@app.route('/create/<int:book_id>/comment',methods=['POST'])
def create_comment(book_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Comment.validate_comment(request.form):
        return redirect(f'/new/{book_id}/comment')
    data = {
        "comment": request.form["comment"],
        "book_id": book_id,
        "user_id": session['user_id']
    }
    Comment.save(data)
    return redirect (f'/book/{book_id}')
