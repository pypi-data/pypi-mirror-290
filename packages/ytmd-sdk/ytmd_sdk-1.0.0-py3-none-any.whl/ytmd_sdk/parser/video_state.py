from .converters import like_status_converter
from .thumbnail import Thumbnail

class VideoState(object):
    author: str = ""
    """author"""
    channel_id: str = ""
    """channel id"""
    title: str = ""
    """title"""
    album: str = ""
    """album"""
    album_id: str = ""
    """album id"""
    like_status: int = 0
    """like status"""
    thumbnails: list[Thumbnail] = []
    """thumbnails"""
    duration_seconds: int = 0
    """duration seconds"""
    id: str = ""
    """id"""

    def __init__(self, data) -> None:
        self.author = data.get("author", "")
        self.channel_id = data.get("channelId", "")
        self.title = data.get("title", "")
        self.album = data.get("album", "")
        self.album_id = data.get("albumId", "")
        self.like_status = like_status_converter.get(data.get("likeStatus", -1), "Unknown")
        self.thumbnails = [Thumbnail(item) for item in data.get("thumbnails", [])]
        self.duration_seconds = data.get("durationSeconds", 0)
        self.id = data.get("id", "")