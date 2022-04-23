import os
from PIL import Image, ImageFilter, ImageEnhance
from bottle import route, run, request, \
    template, static_file
from pydantic import BaseModel, validator, Field
from typing import Optional
from enum import Enum


class Band(str, Enum):
    rgb = 'rgb'
    l = 'l'


class CleanedData(BaseModel):
    height: Optional[int]
    width: Optional[int]
    rotate: Optional[int]
    left_right: Optional[bool]
    top_bottom: Optional[bool]
    band: Band = Field(None)
    blur: Optional[bool]
    minfilter: Optional[bool]
    maxfilter: Optional[bool]
    sharpen: Optional[bool]
    contour: Optional[bool]
    smooth: Optional[bool]
    detail: Optional[bool]
    emboss: Optional[bool]
    find_edges: Optional[bool]
    edge_enhance: Optional[bool]
    brightness: Optional[int]
    color: Optional[int]
    sharpness: Optional[int]
    contrast: Optional[int]

    @validator('*', pre=True)
    def blank_string(cls, value):
        if value == "":
            return None
        return value

    @validator('height', 'width')
    def check_size(cls, value):
        if value:
            if value < 1 or value > 1080:
                raise ValueError('must be within 1-1080 range')
        return value

    @validator('rotate')
    def check_degrees(cls, value):
        if value:
            if value < 1 or value > 360:
                raise ValueError('must be from 1 to 360 degrees')
        return value

    @validator('brightness', 'color', 'sharpness', 'contrast')
    def check_range(cls, value):
        if value:
            if value < 1 or value > 1000:
                raise ValueError('must be from 1 to 1000')
        return value


def convert(percent):
    final = (percent/100)+1
    return final


@route("/")
def main():
    return template("template")

@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    data = CleanedData(**request.params)
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    save_path = os.path.join("./files", upload.filename)
    upload.save(save_path)
    with Image.open(save_path) as im:
        if data.width is not None and data.height is not None:
            box = (data.width, data.height)
            sized = im.resize(box)
        elif data.width is None and data.height is None:
            sized = im
        if data.rotate is not None:
            image = sized.rotate(data.rotate)
        elif data.rotate is None:
            image = sized
        if data.left_right:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if data.top_bottom:
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if data.band == 'rgb':
            image = image.convert('RGB')
        if data.band == 'l':
            image = image.convert('L')
        if data.blur:
            image = image.filter(ImageFilter.BLUR)
        if data.minfilter:
            image = image.filter(ImageFilter.MinFilter)
        if data.maxfilter:
            image = image.filter(ImageFilter.MaxFilter)
        if data.sharpen:
            image = image.filter(ImageFilter.SHARPEN)
        if data.contour:
            image = image.filter(ImageFilter.CONTOUR)
        if data.smooth:
            image = image.filter(ImageFilter.SMOOTH)
        if data.detail:
            image = image.filter(ImageFilter.DETAIL)
        if data.emboss:
            image = image.filter(ImageFilter.EMBOSS)
        if data.edge_enhance:
            image = image.filter(ImageFilter.EDGE_ENHANCE)
        if data.find_edges:
            image = image.filter(ImageFilter.FIND_EDGES)
        if data.brightness is not None:
            img_bright = ImageEnhance.Brightness(image)
            bright_value = convert(data.brightness)
            brightened = img_bright.enhance(bright_value)
        elif data.brightness is None:
            brightened = image
        if data.color is not None:
            img_color = ImageEnhance.Color(brightened)
            color_value = convert(data.color)
            color_enhanced = img_color.enhance(color_value)
        elif data.color is None:
            color_enhanced = brightened
        if data.sharpness is not None:
            img_sharp = ImageEnhance.Sharpness(color_enhanced)
            sharp_value = convert(data.sharpness)
            sharpened = img_sharp.enhance(sharp_value)
        elif data.sharpness is None:
            sharpened = color_enhanced
        if data.contrast is not None:
            img_contrast = ImageEnhance.Contrast(sharpened)
            contrast_value = convert(data.contrast)
            contrasted = img_contrast.enhance(contrast_value)
        elif data.contrast is None:
            contrasted = sharpened
        new_name = "modified" + name + ext
        mod_path = os.path.join("./files", new_name)
        contrasted.save(mod_path)
        return template("template_upload", picture_before=upload.filename, picture_after=new_name)



@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./files")

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./files")





run(reloader=True, debug=True, host='localhost', port=8080)
