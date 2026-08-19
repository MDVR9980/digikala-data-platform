import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER" , "postgres")
    DB_PASS = os.getenv("DB_PASS" , "1234")
    DB_HOST = os.getenv("DB_HOST" , "localhost")
    DB_PORT = os.getenv("DB_PORT" , "5432")
    DB_NAME = os.getenv("DB_NAME" , "digikala_db")

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
