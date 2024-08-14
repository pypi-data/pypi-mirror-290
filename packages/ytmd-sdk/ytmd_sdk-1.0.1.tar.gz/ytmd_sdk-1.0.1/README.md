# Youtube Music Desktop SDK
Simple SDK for controlling [Youtube Music Desktop App](https://ytmdesktop.app/).

## Installation
`pip install ytmd-sdk`

## Example
```python
from YTMDSDK import Events, YTMD, Parser
from time import sleep

ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")

key = ytmd.authenticate() # get token key and sets it at same time
# ytmd.update_token("token") # if you already have a token key you can set it like this

def on_connect():
    print("Connected to YTMD")

def on_disconnect():
    print("Disconnected from YTMD")

def on_error(data):
    print("Error from YTMD: " + data)

def on_state_update(data):
    parser = Parser(data)
    print("Player: " + str(parser.player_state))
    print("Player State: " + parser.player_state.state)
    print("Player video progress: " + str(parser.player_state.video_progress))
    print("Player volume: " + str(parser.player_state.volume))
    print("Player muted: " + str(parser.player_state.muted))
    print("Player ad playing: " + str(parser.player_state.adPlaying))
    print("Player auto play: " + str(parser.player_state.auto_play))
    print("Player is generating: " + str(parser.player_state.isGenerating))
    print("Player is infinite: " + str(parser.player_state.isInfinite))
    print("Player repeat mode: " + parser.player_state.repeatMode)
    print("Player selected item index: " + str(parser.player_state.selectedItemIndex))
    print("Player queue: " + str(parser.player_state.queue))

ytmd.register_event(Events.connect, on_connect)
ytmd.register_event(Events.disconnect, on_disconnect)
ytmd.register_event(Events.error, on_error)
ytmd.register_event(Events.state_update, on_state_update)

ytmd.connect()
sleep(60)
```

## Change Log
```
- 1.0.0: Initial release
```

## Bugs and Suggestions
If you have any bugs or suggestions, feel free to open an issue or a pull request.