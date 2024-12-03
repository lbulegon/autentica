from dotenv import load_dotenv
import os


load_dotenv()

print(os.environ["DB_HOST"])
print(os.environ["APP_SECRET_KEY"])