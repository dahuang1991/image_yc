#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-28 下午8:49
# @Author  : huanggz
# @File    : image.py
# @Software: PyCharm
# code is far away from bugs with the god animal protecting
import base64
import json
import os
import random
import string
import time
from io import BytesIO

from PIL import Image
from flask import Flask, request, make_response,render_template
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.debug=True
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
    img = Image.open(file).convert("RGB")
    # 打水印
    path=os.path.dirname(os.path.realpath(__file__))+'/2018_img/' + str(time.strftime('%m', time.localtime(time.time())))+'/'+str(time.strftime('%d', time.localtime(time.time()))+'/')
    if not os.path.exists(path):
        os.makedirs(path)
    image_name=set_file_name()
    im = add_watermark_to_image(img, Image.open(os.path.dirname(os.path.realpath(__file__))+'/waterr.png').convert("RGBA"))
    im.save( path+image_name+'.jpg')
    return_name  = 'http://47.94.212.232/img/'+str(time.strftime('%m', time.localtime(time.time())))+'/'+str(time.strftime('%d', time.localtime(time.time())))\
            +'/'+image_name+'.jpg'
    result_text=json.dumps({'code':200,'file':return_name})
    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst

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
    imgdata = base64.b64decode(strs)
    file = BytesIO()
    file.write(imgdata)
    img = Image.open(file).convert("RGB")

    # 打水印
    # 打水印
    path = os.path.dirname(os.path.realpath(__file__)) + '/2018_img_end/' + str(
        time.strftime('%m', time.localtime(time.time()))) + '/' + str(
        time.strftime('%d', time.localtime(time.time())) + '/')
    if not os.path.exists(path):
        os.makedirs(path)
    image_name = set_file_name()
    img.save(path + image_name + '.jpg', "JPEG")
    return_name  = 'http://47.94.212.232/img_end/'+str(time.strftime('%m', time.localtime(time.time())))+'/'+str(time.strftime('%d', time.localtime(time.time())))\
            +'/'+image_name+'.jpg'
    result_text=json.dumps({'code':200,'file':return_name})
    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst



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

@app.route('/img/<name>')
def static_img(name):
    image_data = open(os.path.dirname(os.path.realpath(__file__)) + '/static/img/' + name,
                      "rb").read()
    rst = make_response(image_data)
    rst.headers['Content-Type'] = 'image/png'
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst


@app.route('/img/<dir_m>/<dir_d>/<name>')
def img(dir_m,dir_d, name):
    image_data = open(os.path.dirname(os.path.realpath(__file__))+'/2018_img/' + dir_m + '/'+ dir_d + '/' + name, "rb").read()
    rst = make_response(image_data)
    rst.headers['Content-Type'] = 'image/png'
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst

@app.route('/img_end/<dir_m>/<dir_d>/<name>')
def img_end(dir_m,dir_d, name):
    image_data = open(os.path.dirname(os.path.realpath(__file__))+'/2018_img_end/' + dir_m + '/'+ dir_d + '/' + name, "rb").read()
    rst = make_response(image_data)
    rst.headers['Content-Type'] = 'image/png'
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst
@app.route('/')
def html():
    return render_template('explain.html')


if __name__ == '__main__':
    app.run('0.0.0.0',8000)


