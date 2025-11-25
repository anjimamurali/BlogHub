from app import create_app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
import re

def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text).strip('-_')

# Create the Flask application
app = create_app()

# Create an application context
with app.app_context():
    try:
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        print("Creating test user...")
        # Create a test user
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('testpass')
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {user.username} (ID: {user.id})")
        
        print("Creating sample posts...")
        # Create sample posts
        post1 = Post(
            title='First Blog Post',
            slug=slugify('First Blog Post') + '-' + str(int(datetime.utcnow().timestamp())),
            content='This is my first blog post!',
            author_id=user.id
        )
        
        post2 = Post(
            title='Second Blog Post',
            slug=slugify('Second Blog Post') + '-' + str(int(datetime.utcnow().timestamp()) + 1),
            content='Learning Flask with SQLite',
            author_id=user.id
        )
        
        # Add and commit
        db.session.add_all([post1, post2])
        db.session.commit()
        
        print("✅ Seed data inserted successfully!")
        
        # Verify the data was inserted
        print("\nUsers in database:")
        for user in User.query.all():
            print(f"- {user.username} ({user.email}) - ID: {user.id}")
            
        print("\nPosts in database:")
        for post in Post.query.all():
            print(f"- {post.title} (ID: {post.id}) by user ID {post.author_id}")
            print(f"  Slug: {post.slug}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.session.rollback()
        raise  # Re-raise the exception to see the full traceback
