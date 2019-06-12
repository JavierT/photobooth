import os
from resources.h_gallery import GalleryHandler, ImgHandler
from resources.ws_actions import ActionsWebSocket
from resources.h_base import BaseStaticFileHandler


# public_assets = os.path.join(main_path, 'public')
# print('public assets: ', public_assets)
url = '/api/'

api_rest = [
    # Logs frontend
    (url + r"img/(\w+.jpg)/?", ImgHandler),
    (url + r"gallery/?", GalleryHandler)
    #(r"/data/(.*)/?", BaseStaticFileHandler, dict(path=public_assets)),
]
web_socket = [
    (r"/actions/?", ActionsWebSocket)
]
url_patterns = api_rest + web_socket
