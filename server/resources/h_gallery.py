from resources.h_base import BaseHandler
import os
from tornado import gen


class ImgHandler(BaseHandler):

    def get(self, image_name):
        # path = self.static_url("collages/"+ image_name)
        path = "/var/www/photobooth/public/collages/"+ image_name
        print('path: ', path)
        self.write({'url': path})


class GalleryHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_default_headers(self):
        super(GalleryHandler, self).set_default_headers()
        self.set_header("Content-Type", "application/json")

    # @gen.coroutine
    def get(self):
        try:
            # folder = self.application.main_path + '/public/collages/'
            folder = '/var/www/photobooth/public/collages/'
            print('current folder {}'.format(folder))
            imgs = []
            for file in os.listdir(folder):
                if file.endswith('.jpg'):
                    img_json = {
                        'file': file,
                        'url':  file
                    }
                    imgs.append(img_json)
            self.write({'gallery': imgs})
        except Exception as e:
            print(e)
            self.write({'gallery':[]})
