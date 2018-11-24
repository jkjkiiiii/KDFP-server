from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.
def show_image(requet,pic_name):
    image_folder='C:\\Users\\BBfat\\Desktop\\invoice\\spider'
    image_path=os.path.join(image_folder,"images/"+pic_name+".png")
    image_data=open(image_path,"rb").read()

    return HttpResponse(image_data,content_type="image/png")