from .thumbnail import Thumbnail
from typing import Annotated

class queueItem(object):
    title: str = ""
    """title"""
    author: str = ""
    """author"""
    duration: str = ""
    """duration"""
    thumbnails: list[Thumbnail] = []
    """thumbnails"""
    selected: bool = False
    """selected"""
    videoId: str = ""
    """video id"""
    counterparts: None
    """counterparts"""

    def __init__(self, data) -> None:
        self.title = data.get("title", "")
        self.author = data.get("author", "")
        self.duration = data.get("duration", "")
        self.thumbnails = [Thumbnail(item) for item in data['thumbnails']]
        self.selected = data.get("selected", False)
        self.videoId = data.get("videoId", "")
        self.counterparts = data.get("counterparts", None)

    def __str__(self) -> str:
        return str({"Title": self.title,"Author": self.author,"Duration": self.duration,"Thumbnails": self.thumbnails})