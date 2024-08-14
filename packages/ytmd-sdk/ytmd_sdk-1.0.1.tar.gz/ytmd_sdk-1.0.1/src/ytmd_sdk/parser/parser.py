from .player_state import PlayerState
from .video_state import VideoState

class Parser(object):
    player_state: PlayerState = None
    """player state"""

    video_state: VideoState = None
    """video state"""

    def __init__(self, data) -> None:
        self.player_state = PlayerState(data.get("player", {}))
        self.video_state = VideoState(data.get("video", {}))

    def __str__(self) -> str:
        return f"Player: {self.player_state}\nVideo: {self.video_state}"