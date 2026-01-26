from flask import Flask
from routes.post_routes import post_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprint
app.register_blueprint(post_bp)

if __name__ == "__main__":
    app.run(debug=True)
