import os
from dotenv import load_dotenv
load_dotenv()


## DB credentials
DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME = os.environ["POSTGRES_DB"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DB_URL = f'postgresql://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
