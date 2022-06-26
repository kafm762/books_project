from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Book:
    db_name = 'books'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.author = db_data['author']
        self.genre = db_data['genre']
        self.description = db_data['description']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO books (title, author, genre, description, user_id) VALUES (%(title)s,%(author)s,%(genre)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_books = []
        for row in results:
            print(row['title'])
            all_books.append( cls(row) )
        return all_books
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title=%(title)s,author=%(author)s,genre=%(genre)s,description=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_book(books):
        is_valid = True
        if len(books['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","books")
        if len(books['author']) < 3:
            is_valid = False
            flash("Author must be at least 3 characters","books")
        if len(books['genre']) < 3:
            is_valid = False
            flash("Genre must be at least 3 characters", "books")
        if len(books['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","books")
        return is_valid
