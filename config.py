import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")
GENDER, PHOTO, LOCATION, BIO = range(4)
