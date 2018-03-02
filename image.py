#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-28 下午8:49
# @Author  : huanggz
# @File    : image.py
# @Software: PyCharm
# code is far away from bugs with the god animal protecting
import base64
import os,random,string
from io import BytesIO
from PIL import Image
import json
import time
from flask import Flask, request, url_for, Response, make_response

app = Flask(__name__)


@app.route('/save_img', methods=['POST', 'GET'])
def save_img():

    if request.method == 'POST':
        strs = request.form['str']
    else:
        return '参数错误'
    # #接收图片
    imgdata = base64.b64decode(strs)
    file = BytesIO()
    file.write(imgdata)
    img = Image.open(file)
    # 打水印
    path=os.path.dirname(os.path.realpath(__file__))+'/2018_img/' + str(time.strftime('%m', time.localtime(time.time())))+'/'+str(time.strftime('%d', time.localtime(time.time()))+'/')
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    image_name=set_file_name()
    im = add_watermark_to_image(img, Image.open(os.path.dirname(os.path.realpath(__file__))+'/waterr.png'))
    im.save( path+image_name+'.jpg',"JPEG")
    return_name =str(time.strftime('%m', time.localtime(time.time())))+'/'+str(time.strftime('%d', time.localtime(time.time())))\
            +'/'+image_name+'.jpg'
    return json.dumps({'code':200,'file':return_name})

'''
    保存最后的图片
    str  文件的base64
'''


@app.route('/save_img_end', methods=['POST', 'GET'])
def save_img_end():
    if request.method == 'POST':
        strs = request.form['str']
    else:
        return '参数错误'
    # 接收图片
    imgdata = base64.b64decode(str)
    file = BytesIO()
    file.write(imgdata)
    img = Image.open(file)
    if os.path.exists('./2018_img_end/'+str(time.strftime('%m',time.localtime(time.time())))):
        os.mkdir('./2018_img_end/'+str(time.strftime('%m',time.localtime(time.time()))),777)
    # 打水印
    # 打水印
    path = os.path.dirname(os.path.realpath(__file__)) + '/2018_img_end/' + str(
        time.strftime('%m', time.localtime(time.time()))) + '/' + str(
        time.strftime('%d', time.localtime(time.time())) + '/')
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    image_name = set_file_name()
    img.save(path + image_name + '.jpg', "JPEG")
    return json.dumps({'code':200})



def add_watermark_to_image(image, watermark):
    image_x, image_y = image.size
    watermark_x, watermark_y = watermark.size
    # 缩放图片
    scale = 100
    # watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
    # new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = watermark.resize((int(watermark_x * (scale / 100)), int(watermark_y * (scale / 100))),
                                      resample=Image.ANTIALIAS)
    # 透明度z
    watermark_x, watermark_y = rgba_watermark.size
    # 水印位置
    image.paste(rgba_watermark, (image_x - watermark_x - 10, image_y - watermark_y - 3), rgba_watermark)
    return image


def set_file_name():
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_' + ''.join(
        random.sample(string.ascii_letters + string.digits, 8))
    return file_name


@app.route('/img/<dir_m>/<dir_d>/<name>')
def img(dir_m,dir_d, name):
    image_data = open(os.path.dirname(os.path.realpath(__file__))+'/2018_img/' + dir_m + '/'+ dir_d + '/' + name, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    print(name)
    return response


if __name__ == '__main__':
    app.run()


