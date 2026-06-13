from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DB_URL=os.getenv("DATABASE_URL")
print(DB_URL)
engine=create_engine(DB_URL)
print(engine)