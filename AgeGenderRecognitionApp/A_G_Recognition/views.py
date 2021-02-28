import os

from PIL import Image
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .form import UserImage
from .models import UploadedImage
from django.contrib.staticfiles import finders
from tensorflow import keras

dict_age = {'(0, 2)': 0,
            '(4, 6)': 1,
            '(8, 12)': 2,
            '(15, 20)': 3,
            '(25, 32)': 4,
            '(38, 43)': 5,
            '(48, 53)': 6,
            '(60, 100)': 7}


def read_and_resize(filepath):
    im = Image.open(filepath).convert('RGB')
    im = im.resize((227, 227))
    im_array = np.array(im, dtype="uint8")
    im_array = np.array(im_array / 255.0, dtype="float32")
    return im_array


def home(request):
    image = 'static/images/sample.jpeg'
    result = " "
    if request.method == 'POST':
        form = UserImage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # image formatting for prediction
            instance = UploadedImage.objects.last()
            image_full_path = instance.image.path
            imArray = read_and_resize(image_full_path)
            imArray = imArray.reshape(-1, 227, 227, 3)
            # gender prediction
            path = finders.find('model/gender.h5')
            model = keras.models.load_model(path)
            classes = model.predict(imArray)
            if classes[0] > 0.5:
                result = "Gender - Female"
            else:
                result = "Gender - Male"
            # age prediction
            path = finders.find('model/age.h5')
            model = keras.models.load_model(path)
            classes = model.predict(imArray)
            for k, v in dict_age.items():
                if v == np.argmax(classes):
                    result += ", Age - " + k
                    break
            image = '/media/' + str(instance.image)
    form = UserImage()
    return render(request, 'index.html', {'form': form, 'image': image, 'result': result})
