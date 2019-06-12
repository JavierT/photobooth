import logging as log
import tornado
from tornado_cors import CorsMixin


class BaseHandler(CorsMixin, tornado.web.RequestHandler):
#class BaseHandler(tornado.web.RequestHandler):

    CORS_ORIGIN = "*"
    CORS_HEADERS = "Authorization,X-PINGOTHER,Origin,X-Requested-With,Content-Type,Accept"
    CORS_METHODS = "POST, GET, OPTIONS, PUT, DELETE, HEAD"
    CORS_EXPOSE_HEADERS = "Access-Control-Allow-Origin,Access-Control-Allow-Headers"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #CorsMixin.__init__(self)

    def set_default_headers(self):
        super(BaseHandler, self).set_default_headers()
        self.set_header("Content-Type", "application/json")

    def write_error(self, status, msg=None, log_console=False):
        try:
            self.set_status(status)
            if msg:
                self.write({"message": msg})
        except Exception:
            log.critical("BaseHandler/write_error. Erreur \n", exc_info=True)
        # self.finish()

    def get_post_params(self):
        body = self.request.body
        if not self.request.arguments:
            djson = tornado.escape.json_decode(body) if body else {}
        else:
            djson = {k: self.get_argument(k) for k in self.request.arguments}
        return djson


# class BaseStaticFileHandler(tornado.web.StaticFileHandler):
#     pass

class BaseStaticFileHandler(CorsMixin, tornado.web.StaticFileHandler):

    CORS_ORIGIN = "*"
    CORS_METHODS = "POST, PUT, GET, DELETE"
    CORS_HEADERS = "Authorization,X-PINGOTHER,Origin,X-Requested-With,Content-Type,Accept"
    CORS_EXPOSE_HEADERS = "Access-Control-Allow-Origin,Access-Control-Allow-Headers"
