from flask import Flask
from src.routes import routes

app = Flask(__name__)
app.secret_key = "monster-dating-geheimschluessel-2024"
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
