import os
from dotenv import load_dotenv

load_dotenv()

class Envs:
    secret = os.getenv("FLASK_KEY")
    db_uri = os.getenv("DB_URI")

