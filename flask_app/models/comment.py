from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import comment

class Comment:
    database_name = 'books'
    def __init__(self,database_data):
        self.id = database_data['id']
        self.comments = database_data['comments']
        self.user_id = database_data['user_id']
        self.book_id = database_data['book_id']
        self.created_at = database_data['created_at']
        self.updated_at = database_data['updated_at']
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (comments, user_id, book_id) VALUES (%(comments)s,%(user_id)s,%(book_id)s);"
        return connectToMySQL(cls.database_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments;"
        results =  connectToMySQL(cls.database_name).query_db(query)
        all_comments = []
        for row in results:
            print(row['comments'])
            all_comments.append( cls(row) )
        return all_comments
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_book_comments(cls, data):
        query = "SELECT * FROM comments INNER JOIN books WHERE book_id = %(book_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        all_comments = []
        for row in results:
            all_comments.append(cls(row))
        return all_comments
    
    @classmethod
    def update(cls, data):
        query = "UPDATE comments SET comments=%(comments)s, created_at=%(created_at)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query,data)

    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) < 3:
            is_valid = False
            flash("Comment must be at least 3 characters","comments")
        return is_valid

