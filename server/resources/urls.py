import os
from resources.h_gallery import GalleryHandler
from resources.ws_actions import ActionsWebSocket

public_assets = os.path.join(os.path.dirname(__file__), 'static/')
url = '/api/'

api_rest = [
    # Logs frontend
    (url + r"gallery/?", GalleryHandler)
]
web_socket = [
    (r"/actions/?", ActionsWebSocket)
]
url_patterns = api_rest + web_socket
