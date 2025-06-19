from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

HASHTAG_MAP = {
    "basketball": ["#basketball", "#sports", "#hoops"],
    "cooking": ["#cooking", "#food", "#recipe"],
    "gymnastics": ["#gymnastics", "#flexibility", "#athlete"],
    "music": ["#music", "#song", "#performance"],
    "soccer": ["#soccer", "#football", "#goal"],
    "workout": ["#workout", "#fitness", "#exercise"],
}

def generate_hashtags(predicted_class):
    return HASHTAG_MAP.get(predicted_class, ["#video", "#action"])

# from src.yebo import prepare_single_video, sequence_prediction
# # from src.videoClassifier.ipynb import prepare_single_video, sequence_prediction

# sequence_prediction("")

