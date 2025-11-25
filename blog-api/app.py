from app import create_app, db

# Create the Flask app using the factory pattern
app = create_app()

# -----------------------------------
# 5️⃣ Serve React Frontend
# -----------------------------------
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=""):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# -----------------------------------
# 6️⃣ Run App with DB Check
# -----------------------------------
if __name__ == '__main__':
    try:
        print("🔄 Connecting to database...")
        with app.app_context():
            db.create_all()
        print("✅ Database connected and tables created successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)
