## Image processing app

Image processing app allows you to apply various changes on the original image.
Features offered are executed with the Pillow library and include size change, filters, enhancements, color changes, image annotation and others.

###Requirements

The following libraries/modules are required:

- from [Pillow](https://pillow.readthedocs.io/en/stable/index.html#) library:
[Image](https://pillow.readthedocs.io/en/stable/reference/Image.html), [ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html), [ImageFilter](https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html), [ImageEnhance](https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html), [ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html) modules
- [Bottle](https://bottlepy.org/docs/dev/tutorial.html)
- [pydantic](https://pydantic-docs.helpmanual.io/) 
- type Optional from [typing](https://docs.python.org/3/library/typing.html)
module

###Installation

1. To build a docker image:

`docker build -t im-pro-app . `

2. in the *main.py* specify the host the server should listen to and the listening port.

`if __name__ == '__main__':
    run(reloader=True, debug=True, host='0.0.0.0', port=8000)`

3. To run a container with the image, specify mapping of a container port to a port on the Docker host with the `-p` flag:

`docker run -p 8000:8000 im-pro-app`


4. Image processing app is now available on ` http://0.0.0.0:8000/`




