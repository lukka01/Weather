import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,      # ერთდროულად მაქსიმუმ 10 კავშირი
        "max_overflow": 20,
        "pool_recycle": 1800, # 30 წუთში განხალდბა კავშირი
    }