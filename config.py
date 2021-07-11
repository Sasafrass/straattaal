import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # TODO: Change this with above + using the following in a .env file:
        # DATABASE_URL="postgresql:///news_db"
    SQLALCHEMY_DATABASE_URI = "postgresql:///straattaal_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False