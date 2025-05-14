from googleapiclient.discovery import build
import os
from typing import Dict, List

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.service = build("youtube", "v3", developerKey=self.api_key)

    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search videos and return enriched data (with statistics)."""
        # Step 1: Search for videos
        search_response = self.service.search().list(
            q=query,
            part="id,snippet",
            type="video",
            maxResults=max_results
        ).execute()

        video_items = []
        for item in search_response.get("items", []):
            video_id = item["id"]["videoId"]
            # Step 2: Get video details (views, likes, etc.)
            video_response = self.service.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()
            video_data = {
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "channel_title": item["snippet"]["channelTitle"],
                "views": int(video_response["items"][0]["statistics"].get("viewCount", 0)),
                "likes": int(video_response["items"][0]["statistics"].get("likeCount", 0)),
            }
            video_items.append(video_data)
        return video_items