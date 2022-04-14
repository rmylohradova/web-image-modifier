from bottle import route, run, request,\
    template, response, get, static_file, post, error, redirect, abort
import os
from PIL import Image

@route("/")
def main():
    return template("template")

@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    width = request.params.get('width')
    height = request.params.get('height')
    rotate = request.params.get('rotate')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'
    save_path = os.path.join("./files", upload.filename)
    upload.save(save_path)
    with Image.open(save_path) as im:
        if width != '' and height != '':
            box = (int(width), int(height))
            sized = im.resize(box)
        elif width == '' and height == '':
            sized = im
        if rotate != '':
            image = sized.rotate(int(rotate))
        elif rotate == '':
            image = sized
        if request.params.get('left-right'):
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if request.params.get('top-bottom'):
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if request.params.get('band') == 'RGB':
            image = image.convert('RGB')
        if request.params.get('band') == 'L':
            image = image.convert('L')
        new_name = "modified" + name + ext
        mod_path = os.path.join("./files", new_name)
        image.save(mod_path)
        return template("template_upload", picture_before=upload.filename, picture_after=new_name)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./files")

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root="./files")





run(reloader=True, debug=True, host='localhost', port=8080)
