import os
import urllib.parse

from dotenv import load_dotenv

load_dotenv(".env")

name_application: str = os.getenv("NAME_APPLICATION")
version_application: str = os.getenv("VERSION_APPLICATION")
main_url: str = os.getenv("MAIN_URL")
host_value: str = os.getenv("POSTGRES_HOST")
port_value: str = os.getenv("POSTGRES_PORT")
database_value: str = os.getenv("POSTGRES_DB")
user_value: str = urllib.parse.quote_plus(os.getenv("POSTGRES_USER"))
password_value: str = urllib.parse.quote_plus(os.getenv("POSTGRES_PASSWORD"))

