from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from string import ascii_letters
import textwrap


def convert(percent):
    final = (percent/100)+1
    return final


def apply_font(font):
    if font == "arial":
        font_file = 'arial.ttf'
    elif font == "cursive":
        font_file = 'cursive.ttf'
    elif font == 'bold':
        font_file = 'COOPBL.ttf'
    elif font == 'hello_kitty':
        font_file = 'hellokitty.ttf'
    return font_file


def multi_text_center(txt, txt_color, img, txt_size, font):
    dctx = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(apply_font(font), txt_size)
    avg_char_width = sum(fnt.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int(img.width/ avg_char_width)
    text = textwrap.fill(text=txt, width=max_char_count)
    dctx.text(
        (img.width / 2, img.height/2),
        text,
        font=fnt,
        fill=txt_color,
        anchor='mm',
        align='center'
    )

def one_line_text(txt, txt_color, img, txt_size, font, place):
    dctx = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(apply_font(font), txt_size)
    if place == 'top_center':
        dctx.text(
            (img.width / 2, 0 + 10),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='ma',
        )
    if place == 'bottom_center':
        dctx.text(
            (img.width / 2, img.height - 10),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='mb',
        )
    if place == 'center_left':
        dctx.text(
            (0+10, img.height / 2),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='ls',
        )
    if place == 'center_right':
        dctx.text(
            (img.width-10, img.height / 2),
            txt,
            font=fnt,
            fill="white",
            anchor='rs',
        )


def maybe_resize(width, height, image):
    if width and height:
        box = (width, height)
        sized = image.resize(box)
        return sized
    elif width is None and height is None:
        return image


def maybe_rotate(degree, image):
    if degree:
        rotated = image.rotate(degree)
        return rotated
    elif degree is None:
        return image


def maybe_brighten(value, image):
    if value:
        img_bright = ImageEnhance.Brightness(image)
        bright_value = convert(value)
        brightened = img_bright.enhance(bright_value)
        return brightened
    if value is None:
        return image


def maybe_enhance_color(value, image):
    if value:
        img_color = ImageEnhance.Color(image)
        color_value = convert(value)
        color_enhanced = img_color.enhance(color_value)
        return color_enhanced
    elif value is None:
        return image


def maybe_sharpen(value, image):
    if value:
        img_sharp = ImageEnhance.Sharpness(image)
        sharp_value = convert(value)
        sharpened = img_sharp.enhance(sharp_value)
        return sharpened
    elif value is None:
        return image


def maybe_enhance_contrast(value, image):
    if value:
        img_contrast = ImageEnhance.Contrast(image)
        contrast_value = convert(value)
        contrasted = img_contrast.enhance(contrast_value)
        return contrasted
    elif value is None:
        return image


def maybe_filter(image, blur, minfilter, maxfilter, sharpen, contour, smooth, detail, emboss, edge_enhance, find_edges):
    if blur:
        image = image.filter(ImageFilter.BLUR)
    if minfilter:
        image = image.filter(ImageFilter.MinFilter)
    if maxfilter:
        image = image.filter(ImageFilter.MaxFilter)
    if sharpen:
        image = image.filter(ImageFilter.SHARPEN)
    if contour:
        image = image.filter(ImageFilter.CONTOUR)
    if smooth:
        image = image.filter(ImageFilter.SMOOTH)
    if detail:
        image = image.filter(ImageFilter.DETAIL)
    if emboss:
        image = image.filter(ImageFilter.EMBOSS)
    if edge_enhance:
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    if find_edges:
        image = image.filter(ImageFilter.FIND_EDGES)
    return image

def maybe_change_color(color, image):
    if color:
        r, g, b = image.split()
    if color == 'pink':
        image = Image.merge("RGB", (r, b, g))
    if color == 'blue':
        image = Image.merge("RGB", (b, g, r))
    if color == 'green':
        image = Image.merge("RGB", (g, r, b))
    return image


def process_image(im, data):
    im = maybe_resize(data.height, data.width, im)
    im = maybe_rotate(data.rotate, im)
    if data.left_right:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if data.top_bottom:
        im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if data.band == 'rgb':
        im = im.convert('RGB')
    if data.band == 'l':
        im = im.convert('L')
    im = maybe_filter(im, data.blur, data.minfilter, data.maxfilter,
                      data.sharpen, data.contour, data.smooth, data.detail,
                      data.emboss, data.edge_enhance, data.find_edges)
    im = maybe_brighten(data.brightness, im)
    im = maybe_enhance_color(data.color, im)
    im = maybe_sharpen(data.sharpness, im)
    im = maybe_enhance_contrast(data.contrast, im)
    im = maybe_change_color(data.merged_bands, im)
    if data.on_text:
        txt = data.on_text
        if data.text_placement == 'center':
            multi_text_center(txt, data.text_color, im, data.text_size, data.font)
        else:
            one_line_text(txt, data.text_color, im, data.text_size, data.font, data.text_placement)
    return im