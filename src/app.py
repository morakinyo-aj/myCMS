from flask import Flask
from utils import db, login_manager, bcrypt
from models.models import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and initialize routes
from routes.auth import init_auth_routes
from routes.main import init_main_routes

init_auth_routes(app)
init_main_routes(app)

if __name__ == "__main__":
    app.run(port=8080)

