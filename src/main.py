from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube Video Finder!"}