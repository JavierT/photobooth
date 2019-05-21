from flask_restful import Resource
from flask import current_app as app
from flask import Flask, send_file
import os

class Image(Resource):
    def get(self, image_name):
        print('searching : ', image_name)
        return app.send_static_file(image_name) #, mimetype='image/jpg')

class Gallery(Resource):
    def get(self):
        try:
            folder = app.static_folder
            print('current folder {}'.format(folder))
            imgs = []
            for file in os.listdir(folder):
                if file.endswith('.jpg'):
                    img_json = {
                        'file': file,
                        'url':  file
                    }
                    imgs.append(img_json)
            return {'gallery': imgs}
        except Exception as e:
            print(e)
            return {'gallery':[]} 