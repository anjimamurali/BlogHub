# BlogHub

A full-stack blogging platform built with React and Flask, featuring user authentication, blog post management, and a clean, responsive interface.

## Features

- 🚀 **User Authentication**: Register, login, and manage user profiles
- ✍️ **Blog Management**: Create, read, update, and delete blog posts
- 🔍 **Search & Filter**: Find posts by title, author, or tags
- 💬 **Comments**: Leave and manage comments on blog posts
- 🎨 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🔒 **Secure**: Password hashing and protected routes

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- SQLite (included with Python)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anjimamurali/BlogHub.git
   cd BlogHub
   ```

2. **Set up the backend**
   ```bash
   # Navigate to backend directory
   cd blog-api
   
   # Create and activate virtual environment
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   # Navigate to frontend directory
   cd ../blog-frontend
   
   # Install dependencies
   npm install
   ```

## Configuration

1. **Backend Environment Variables**
   Create a `.env` file in the `blog-api` directory with the following variables:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URI=sqlite:///blog.db
   ```

## Running the Application

1. **Start the backend server**
   ```bash
   # From blog-api directory
   python run.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the frontend development server**
   ```bash
   # From blog-frontend directory
   npm start
   ```
   The application will open in your default browser at `http://localhost:3000`

## Project Structure

```
BlogHub/
├── blog-api/                 # Backend (Flask)
│   ├── app/                  # Application package
│   ├── migrations/           # Database migrations
│   ├── .env                  # Environment variables
│   ├── requirements.txt      # Python dependencies
│   └── run.py               # Application entry point
│
└── blog-frontend/           # Frontend (React)
    ├── public/              # Static files
    ├── src/                 # React source code
    ├── package.json         # Node.js dependencies
    └── ...
```

## API Documentation

API documentation is available at `http://localhost:5000/api` when the backend server is running.

## Testing

### Backend Tests
```bash
# From blog-api directory
python -m pytest
```

### Frontend Tests
```bash
# From blog-frontend directory
npm test
```

## Deployment

### Backend
1. Set up a production WSGI server (e.g., Gunicorn, uWSGI)
2. Configure a production database (PostgreSQL recommended)
3. Set up environment variables for production

### Frontend
```bash
# From blog-frontend directory
npm run build
```
Deploy the contents of the `build` directory to your static file hosting service.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by Anjima A.M
