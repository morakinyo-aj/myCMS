from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

HASHTAG_MAP = {
    "ApplyEyeMakeup": ["#makeup", "#beauty", "#eyemakeup"],
    "ApplyLipstick": ["#lipstick", "#makeuplooks", "#cosmetics"],
    "Archery": ["#archery", "#bowandarrow", "#target"],
    "BabyCrawling": ["#baby", "#crawlingbaby", "#cutebabies"],
    "BalanceBeam": ["#gymnastics", "#balance", "#beamwork"],
    "BandMarching": ["#marchingband", "#bandlife", "#parade"],
    "BaseballPitch": ["#baseball", "#pitching", "#sportsclip"],
    "Basketball": ["#basketball", "#hoops", "#dunk"],
    "BasketballDunk": ["#basketball", "#slam", "#dunkcontest"],
    "BenchPress": ["#benchpress", "#gymmotivation", "#liftheavy"]
}

def generate_hashtags(predicted_class):
    return HASHTAG_MAP.get(predicted_class, ["#video", "#action"])

# from src.yebo import prepare_single_video, sequence_prediction
# # from src.videoClassifier.ipynb import prepare_single_video, sequence_prediction

# sequence_prediction("")

