from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
import time
from datetime import datetime, timedelta
from . import db
from .models import User, Post, Comment
from .auth import token_required, admin_required, author_required

bp = Blueprint('api', __name__)

# -------------------- Public Routes --------------------
@bp.route('/')
def home():
    return jsonify({"message": "Blog API is running"})

@bp.route('/debug/routes')
def debug_routes():
    """Debug endpoint to list all registered routes"""
    from flask import current_app
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({'routes': routes})

# -------------------- Authentication Routes --------------------
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate auth token
    token = new_user.generate_auth_token()
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': getattr(new_user, 'role', 'user')
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Generate token
    token = user.generate_auth_token()
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })

# -------------------- Post Routes --------------------
@bp.route('/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    # Admins can see all posts, others only see published posts
    if current_user.is_admin():
        posts = Post.query.all()
    else:
        posts = Post.query.filter_by(published=True).all()
    
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'excerpt': post.content[:150] + '...' if len(post.content) > 150 else post.content,
        'author': post.author.username,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat() if post.updated_at else None
    } for post in posts])

@bp.route('/posts', methods=['POST'])
@token_required
@author_required
def create_post(current_user):
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content are required'}), 400
    
    # Generate slug
    slug = f"{data['title'].lower().replace(' ', '-')}-{int(time.time())}"
    
    new_post = Post(
        title=data['title'],
        content=data['content'],
        slug=slug,
        author_id=current_user.id,
        published=data.get('published', False)
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        'message': 'Post created successfully',
        'post': {
            'id': new_post.id,
            'title': new_post.title,
            'slug': new_post.slug,
            'published': new_post.published
        }
    }), 201

# -------------------- Comment Routes --------------------
@bp.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    # Only show unpublished posts to admins or the author
    if not post.published and not (current_user.is_admin() or current_user.id == post.author_id):
        return jsonify({'message': 'Post not found'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'slug': post.slug,
        'published': post.published,
        'author': {
            'id': post.author.id,
            'username': post.author.username
        },
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat() if post.updated_at else None,
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'created_at': comment.created_at.isoformat()
        } for comment in post.comments]
    })

@bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    # Only allow author or admin to update
    if current_user.id != post.author_id and not current_user.is_admin():
        return jsonify({'message': 'Not authorized to update this post'}), 403
    
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'published' in data and (current_user.is_admin() or current_user.id == post.author_id):
        post.published = data['published']
    
    post.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Post updated successfully'})

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    # Only allow author or admin to delete
    if current_user.id != post.author_id and not current_user.is_admin():
        return jsonify({'message': 'Not authorized to delete this post'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'})

@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    # Can't comment on unpublished posts unless admin or author
    if not post.published and not (current_user.is_admin() or current_user.id == post.author_id):
        return jsonify({'message': 'Cannot comment on unpublished posts'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'message': 'Comment content is required'}), 400
    
    new_comment = Comment(
        content=data['content'],
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment': {
            'id': new_comment.id,
            'content': new_comment.content,
            'author': current_user.username,
            'created_at': new_comment.created_at.isoformat()
        }
    }), 201

# Admin routes
@bp.route('/admin/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat(),
        'post_count': len(user.posts)
    } for user in users])

@bp.route('/admin/users/<int:user_id>/role', methods=['PUT'])
@token_required
@admin_required
def update_user_role(current_user, user_id):
    if current_user.id == user_id:
        return jsonify({'message': 'Cannot change your own role'}), 400
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'role' not in data or data['role'] not in User.ROLES:
        return jsonify({'message': 'Invalid role'}), 400
    
    user.role = data['role']
    db.session.commit()
    
    return jsonify({
        'message': 'User role updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    })
