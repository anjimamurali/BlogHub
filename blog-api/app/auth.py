from functools import wraps
from flask import request, jsonify, current_app
import jwt
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Verify token
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': 'Could not verify token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            if not current_user.has_role(role_name):
                return jsonify({
                    'message': f'This action requires {role_name} role!'
                }), 403
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

# Common role decorators
admin_required = role_required('admin')
author_required = role_required('author')
