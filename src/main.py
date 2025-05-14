from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from src.services.youtube_client import YouTubeClient
from fastapi import FastAPI, HTTPException
from src.services.youtube_client import YouTubeClient
from src.services.data_storage import JSONStorage
from src.utils.data_cleaner import clean_video_data
from src.services.prediction_service import CategoryClassifier
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
 
app = FastAPI()

# Add this Pydantic model
class VideoData(BaseModel):
    title: str
    description: str

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

@app.get("/search-and-save")
def search_and_save(query: str, max_results: int = 10):
    try:
        # 1. Fetch data from YouTube
        youtube = YouTubeClient()
        raw_videos = youtube.search_videos(query, max_results)
        
        # 2. Clean data
        cleaned_videos = [clean_video_data(video) for video in raw_videos]
        
        # 3. Save to storage
        storage = JSONStorage()
        storage.save(cleaned_videos, query)
        
        return {"status": "success", "query": query, "saved_items": len(cleaned_videos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Add new endpoint
# Update the endpoint
@app.post("/predict-category")
def predict_category(video_data: VideoData):  # Use the Pydantic model as parameter
    try:
        classifier = CategoryClassifier()
        category = classifier.predict_category(video_data.title, video_data.description)
        return {
            "title": video_data.title,
            "predicted_category": category
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))