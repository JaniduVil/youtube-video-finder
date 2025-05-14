import re
from typing import Dict

def clean_video_data(video_data: Dict) -> Dict:
    """Clean and transform raw YouTube API data."""
    # Clean title/description (remove special chars, extra spaces)
    video_data["title"] = re.sub(r"[^\w\s]", "", video_data["title"]).strip()
    video_data["description"] = re.sub(r"\s+", " ", video_data["description"]).strip()

    # Convert published_at to datetime (optional)
    # video_data["published_at"] = pd.to_datetime(video_data["published_at"])

    return video_data