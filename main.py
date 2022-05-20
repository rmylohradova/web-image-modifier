import os
from PIL import Image
from bottle import route, run, request, \
    template, static_file
from pydantic import BaseModel, validator, Field
from typing import Optional
from enum import Enum
from process_im_lib import process_image


class Band(str, Enum):
    rgb = 'rgb'
    l = 'l'


class MergedBand(str, Enum):
    pink = 'pink'
    blue = 'blue'
    green = 'green'


class TextPlacement(str, Enum):
    center = 'center'
    top_center = 'top_center'
    bottom_center = 'bottom_center'
    center_left = 'center_left'
    center_right = 'center_right'


class TextFont(str, Enum):
    arial = 'arial'
    bold = 'bold'
    cursive = 'cursive'
    motion_picture = 'motion_picture'
    southern_aire = 'southern_aire'


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
    merged_bands: MergedBand = Field(None)
    on_text: Optional[str]
    text_color: Optional[str]
    text_placement: TextPlacement = Field('center')
    text_size: Optional[int]
    font: TextFont = Field('arial')

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

    @validator('brightness', 'color', 'sharpness', 'contrast', 'text_size')
    def check_range(cls, value):
        if value:
            if value < 1 or value > 1000:
                raise ValueError('must be from 1 to 1000')
        return value


@route("/")
def main():
    return template("templates/template.html")


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
        im = process_image(im, data)
        new_name = upload.filename
        mod_path = os.path.join("./modified", new_name)
        im.save(mod_path)
    return template("templates/template_upload.html", picture_before=upload.filename, picture_after=new_name, size=im.size)


@route('/history/<filename>')
def show_images(filename):
    name, ext = os.path.splitext(filename)
    return template('template/single_history.html', picture_before=filename, picture_after=filename, picture_name=name)


@route('/history')
def show_all():
    original = []
    for filename in os.listdir('files/'):
            original.append(filename)
    return template('templates/history.html', original=original)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./files")


@route('/static/modified/<filename>')
def server_static(filename):
    return static_file(filename, root="./modified")


if __name__ == '__main__':
    run(reloader=True, debug=True, host='0.0.0.0', port=8000)
