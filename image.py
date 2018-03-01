#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-28 下午8:49
# @Author  : huanggz
# @File    : image.py
# @Software: PyCharm
# code is far away from bugs with the god animal protecting
import base64
import os
from io import BytesIO
from PIL import Image

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
    img.show()
    # 打水印
    im = add_watermark_to_image(img, Image.open('./waterr.png'))
    im.show()
    return 'Hello World!'


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
    # 打水印
    img.save('2.jpg')
    return 'Hello World!'


def add_watermark_to_image(image, watermark):
    image_x, image_y = image.size
    watermark_x, watermark_y = watermark.size
    # 缩放图片
    scale = 100
    # watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
    # new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = watermark.resize((int(watermark_x * (scale / 100)), int(watermark_y * (scale / 100))),
                                      resample=Image.ANTIALIAS)
    # 透明度
    watermark_x, watermark_y = rgba_watermark.size
    # 水印位置
    image.paste(rgba_watermark, (image_x - watermark_x - 10, image_y - watermark_y - 3), rgba_watermark)
    return image


@app.route('/img/<dir_name>/<name>')
def img(dir_name, name):
    image_data = open('./' + dir_name + '/' + name, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    print(name)
    return response


if __name__ == '__main__':
    app.run()
