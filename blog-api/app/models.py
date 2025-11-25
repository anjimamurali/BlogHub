# from . import db
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# # import jwt
# from flask import current_app
# from functools import wraps

# class User(db.Model):
#     __tablename__ = 'users'
    
#     # Roles
#     ROLES = {
#         'admin': 3,
#         'author': 2,
#         'user': 1
#     }
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.Text, nullable=False)
#     role = db.Column(db.String(20), default='user', nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
#     comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def generate_auth_token(self, expires_in=3600):
#         """Generate JWT token for the user"""
#         return jwt.encode(
#             {'user_id': self.id, 'exp': datetime.utcnow() + datetime.timedelta(seconds=expires_in)},
#             current_app.config['SECRET_KEY'],
#             algorithm='HS256'
#         )
    
#     def has_role(self, role_name):
#         """Check if user has the specified role"""
#         return self.ROLES.get(self.role, 0) >= self.ROLES.get(role_name, 0)
    
#     def is_admin(self):
#         return self.has_role('admin')
    
#     def is_author(self):
#         return self.has_role('author') or self.is_admin()
    
#     @staticmethod
#     def verify_auth_token(token):
#         """Verify JWT token and return user if valid"""
#         try:
#             data = jwt.decode(
#                 token,
#                 current_app.config['SECRET_KEY'],
#                 algorithms=['HS256']
#             )
#             return User.query.get(data['user_id'])
#         except:
#             return None

# class Post(db.Model):
#     __tablename__ = 'posts'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(255), nullable=False)
#     slug = db.Column(db.String(255), unique=True, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     published = db.Column(db.Boolean, default=False, nullable=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'slug': self.slug,
#             'content': self.content,
#             'published': self.published,
#             'author_id': self.author_id,
#             'created_at': self.created_at.isoformat(),
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None,
#             'comment_count': len(self.comments)
#         }

# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
#     def __repr__(self):
#         return f'<Post {self.title}>'

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    # Role hierarchy
    ROLES = {
        'admin': 3,
        'author': 2,
        'user': 1
    }
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Auth token helpers
    def generate_auth_token(self, expires_in=3600):
        """Generate JWT token for the user"""
        import jwt
        from flask import current_app
        from datetime import datetime, timedelta
        return jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return user if valid"""
        import jwt
        from datetime import datetime
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(data['user_id'])
        except:
            return None
    
    # Role-based helpers
    def has_role(self, role_name):
        """Check if user has the specified role"""
        return self.ROLES.get(self.role, 0) >= self.ROLES.get(role_name, 0)
    
    def is_admin(self):
        return self.has_role('admin')
    
    def is_author(self):
        return self.has_role('author') or self.is_admin()
    
    # Serialize user for JSON response
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'published': self.published,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comment_count': len(self.comments)
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'
