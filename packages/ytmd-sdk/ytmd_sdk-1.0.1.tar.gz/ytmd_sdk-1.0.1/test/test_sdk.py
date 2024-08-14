import unittest
from unittest.mock import patch
from ytmd_sdk import YTMD
from requests import Session

class TestYTMD(unittest.TestCase):
    def test_authenticate(self):
        with patch.object(Session, "post") as session_mock:
            ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")
            session_mock.return_value.status_code = 400
            session_mock.return_value.text = "Unittest"
            self.assertRaises(Exception, ytmd.authenticate)

    def test_get_version(self):
        with patch.object(Session, "get") as session_mock:
            ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")
            session_mock.return_value.status_code = 200
            session_mock.return_value.json.return_value = {"apiVersions": ["v1"]}
            response = ytmd.get_version()
            self.assertEqual(response, ["v1"])

    def test_get_state(self):
        with patch.object(Session, "get") as session_mock:
            ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")
            self.assertRaises(Exception, ytmd.get_state) # no token

            ytmd.update_token("token")
            session_mock.return_value.status_code = 200
            self.assertEqual(ytmd.get_state().status_code, 200)

    def test_ytmd_method(self):
        methods = ["get_playlists", "play", "pause", "volume_up", "volume_down", 
                   "set_volume", "mute", "unmute", "seek_to", "next", "previous", 
                   "repeatMode", "shuffle", "play_index", "toggle_like", "toggle_dislike"]
        
        for method in methods:
            with patch.object(Session, "post") as session_mock:
                print("Testing method: " + method)
                ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")

                if method in ["set_volume", "seek_to", "repeatMode", "play_index"]:
                    self.assertRaises(Exception, getattr(ytmd, method), 1)
                    ...
                else:
                    self.assertRaises(Exception, getattr(ytmd, method)) # no token

                ytmd.update_token("token")
                session_mock.return_value.status_code = 200

                if method in ["set_volume", "seek_to", "repeatMode", "play_index"]:
                    # response = getattr(ytmd, method)(1)
                    ...
                else:
                    response = getattr(ytmd, method)()
                    self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()