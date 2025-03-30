import os

from dotenv import load_dotenv

load_dotenv()

# Environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "inventory")
USERS_PATH = os.getenv("USERS_PATH")
BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
CREATE_DELIVERY_TOPIC = os.getenv("CREATE_DELIVERY_TOPIC", "rpc_create_delivery")
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost,"
    "http://localhost:4200,"
    "https://appstaff-dot-ccp-perspicapps.uc.r.appspot.com",
).split(",")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
