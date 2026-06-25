from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)

