import os

shhh = os.environ.get(['SECRET_KEY'])

heroku_db_connect = os.environ.get(['DATABASE_URL'])