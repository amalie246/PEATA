import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")

#Testing connecting to another open-source API
response = requests.get("https://api.github.com")

#Status code
print("Response: %d" % response.status_code)

#Response content, JSON format
print(response.content)

#Getting specific headers
print("Content type: ", end="")
print(response.headers["Content-Type"])