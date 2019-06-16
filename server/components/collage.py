from PIL import Image
import random
from datetime import date
import os

#based on https://stackoverflow.com/questions/35438802/making-a-collage-in-pil

class Collage():

    cols = 2
    rows = 2

    path_thumbnails = '/var/www/html/thumbnails/'
    path_fullimage = '/var/www/html/collage/'
    path_photos = '/home/pi/photo_tmp/'

    def __init__(self, width, heigth, margin):
        self.enum_functions = {
            0: self.filter0,
            1: self.filter1,
            2: self.filter2,
            3: self.filter0,  # filter3 removed, too much noise
            4: self.filter0,  # filter4 removed, too yellow
            5: self.filter5
        }
        self.a_images = []
        self.new_im = Image.new('RGB', (width, heigth))
        self.margin = margin
        self.thumbnail_width = (width - margin) // self.cols
        self.thumbnail_height = (heigth - margin) // self.rows
        self.size = self.thumbnail_width, self.thumbnail_height

    def create(self, path, listofimages):
        #listofimages=['Image1.jpg', 'Image2.jpg', 'Image3.jpg', 'Image4.jpg']
        self.a_images = listofimages
        self.path = path
        for img in listofimages:
            self.create_effect(img)
        return self.create_collage()

    def create_effect(self, image_name):
        im= Image.open(self.path + image_name)
        im.thumbnail(self.size)
        degree = random.randint(0,10)
        degree = 0 if degree < 5 else degree - 5
        
        function = self.enum_functions[degree]
        print('executing filter: ', function)
        out_image = function(im)
        out_image.save(self.path + "_"+image_name)

    def create_thumbnail(self, img_name):
        im = Image.open(self.path_fullimage + img_name)
        im.thumbnail(self.size)
        im.save(self.path_thumbnails + img_name)

    def create_collage(self):
        #listofimages=['_Image1.jpg', '_Image2.jpg', '_Image3.jpg', '_Image4.jpg']
        ims = []
        for p in self.a_images:
            im = Image.open(self.path + "_" + p)          
            ims.append(im)
        i = 0
        x = 0
        y = 0
        for col in range(self.cols):
            for row in range(self.rows):
                print(i, x, y)
                self.new_im.paste(ims[i], (x, y))
                i += 1
                y += self.thumbnail_height + self.margin
            x += self.thumbnail_width 
            y = 0
        now = date.now()
        str_date = now.strftime("%d_%m_%y_%H_%M_%S")
        img_name =  str_date + '.jpg'
        print('saving image with name: ', img_name)
        self.new_im.save(self.path_fullimage + img_name)
        self.create_thumbnail(img_name)
        self.clean()
        return img_name

    def bck_picts(self, listofimages):  
        # TODO! 
        for img in listofimages:
            os.rename(self.path + img, self.path_bck + img )
            os.remove(self.path + img)
            os.remove(self.path + "_"+ img)
        self.a_images = []  

    def clean(self):
        for img in self.a_images:
            os.remove(self.path + img)
            os.remove(self.path + "_"+ img)
        self.a_images = []

    def filter0(self, im):
        return im

    def filter1(self, im):
        return im.convert("RGB", (
            0.9756324, 0.154789, 0.180423, 0,
            0.212671, 0.715160, 0.254783, 0,
            0.123456, 0.119193, 0.950227, 0 ))

    def filter2(self, im):
        return im.convert("RGB", (
            0.412453, 0.357580, 0.180423, 0,
            0.212671, 0.715160, 0.072169, 0,
            0.019334, 0.119193, 0.950227, 0 ))
        
    def filter3(self, im):
        return im.convert("1")

    def filter4(self, im):
        return im.convert("RGB", (
            0.986542, 0.154789, 0.756231, 0,
            0.212671, 0.715160, 0.254783, 0,
            0.123456, 0.119193, 0.112348, 0 ))

    def filter5(self, im):
        out4= im.convert("RGB", (
            0.986542, 0.154789, 0.756231, 0,
            0.212671, 0.715160, 0.254783, 0,
            0.123456, 0.119193, 0.112348, 0 ))
        return Image.blend(im, out4, 0.5)


    
