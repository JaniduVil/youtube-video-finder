from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from src.services.youtube_client import YouTubeClient

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
 
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube Video Finder!"}

@app.get("/search")
def search_videos(query: str, max_results: int = 10):
    try:
        youtube = YouTubeClient()
        results = youtube.search_videos(query, max_results)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))