from flask import Flask
from routes.post_routes import post_bp
from validation_module.routes import validation_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(post_bp)
app.register_blueprint(validation_bp)

if __name__ == "__main__":
    app.run(debug=True)
