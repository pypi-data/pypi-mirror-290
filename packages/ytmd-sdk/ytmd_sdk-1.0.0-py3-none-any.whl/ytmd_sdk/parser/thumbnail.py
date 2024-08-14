class Thumbnail(object):
    url: str = ""
    """url"""
    width: int = 0
    """width"""
    height: int = 0
    """height"""

    def __init__(self, data) -> None:
        self.url = data.get("url", "")
        self.width = data.get("width", 0)
        self.height = data.get("height", 0)

    def __str__(self) -> str:
        return str({"URL": self.url,"Width": self.width,"Height": self.height})