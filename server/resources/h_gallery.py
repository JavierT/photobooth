from resources.h_base import BaseHandler


class GalleryHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_default_headers(self):
        super(GalleryHandler, self).set_default_headers()
        self.set_header("Content-Type", "application/json")

    def get(self):
        print('Request get for gallery!')
        self.write("Hello, world")