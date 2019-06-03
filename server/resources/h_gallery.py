import tornado

class GalleryHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_default_headers(self):
        super(GalleryHandler, self).set_default_headers()
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.write("Hello, world")