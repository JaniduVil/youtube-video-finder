from googleapiclient.discovery import build
import os

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.service = build("youtube", "v3", developerKey=self.api_key)

    def search_videos(self, query: str, max_results: int = 10):
        request = self.service.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        return response