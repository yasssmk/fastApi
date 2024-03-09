from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/ysamk/Desktop/coding/API course/app/.env")

import os



class Settings():
    database_hostname = os.getenv("DATABASE_HOSTNAME")
    database_port = os.getenv("DATABASE_PORT")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_name = os.getenv("DATABASE_NAME")
    database_username = os.getenv("DATABASE_USERNAME")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")



settings = Settings()

# database_hostname = os.getenv("DATABASE_HOSTNAME")
# database_port = os.getenv("DATABASE_PORT")
# database_password = os.getenv("DATABASE_PASSWORD")
# database_name = os.getenv("DATABASE_NAME")
# database_username = os.getenv("DATABASE_USERNAME")
# secret_key = os.getenv("SECRET_KEY")
# algorithm = os.getenv("ALGORITHM")
# access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# print(f"test: {algorithm}")