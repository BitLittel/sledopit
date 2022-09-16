from PIL import Image
import os

WORKDIR = os.path.dirname(os.path.realpath(__file__))
DIR_IMG = os.path.join(WORKDIR, "main/static/img/reseach_img")
photo_format = ['jpeg', 'png', 'webp']

onlyfiles = [f for f in os.listdir(DIR_IMG) if os.path.isfile(os.path.join(DIR_IMG, f))]

for i in onlyfiles:
    if i.split('.')[1] in photo_format:
        print(i)
        path_photo = os.path.join(DIR_IMG, i)
        img = Image.open(path_photo)
        img.save(path_photo, quality=60)
