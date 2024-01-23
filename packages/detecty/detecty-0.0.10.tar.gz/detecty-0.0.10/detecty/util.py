from pathlib import Path

from PIL import Image, ImageDraw, ImageFile
from torch import Tensor
from torchvision.transforms.functional import (pad, resize, to_grayscale,
                                               to_tensor)

from detecty.bbox import Bbox

ImageFile.LOAD_TRUNCATED_IMAGES = True


def load_img(path: str | Path):
    return to_grayscale_tensor(Image.open(path))


def draw_bbox(img: Image.Image, *bboxs: Bbox):
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    for color, bb in zip(colors, bboxs):
        draw.rectangle(
            (bb.x1, bb.y1, bb.x2, bb.y2),
            outline=color,
            width=3)

    return img


def to_grayscale_tensor(img: Image.Image):
    return to_tensor(to_grayscale(img))


def pad_square(img: Tensor):
    _, h, w = img.shape

    if h == w:
        return img

    if h > w:
        return pad(img, [0, 0, h-w, 0])

    return pad(img, [0, 0, 0, w-h])


def resize_square(img: Tensor, target_size=256):
    _, h, w = img.shape

    assert h == w, f'Image is not square: {h} != {w}'

    img = resize(img, [target_size, target_size], antialias=True)

    return img


def pad_resize_scale_bb(img: Tensor, bb: Bbox, target_size=256):
    img = pad_square(img)
    _, h, w = img.shape
    scale = target_size / h
    img = resize_square(img, target_size)

    return img, bb.scale(scale).tensor


def clear_tmp():
    from os import mkdir
    from shutil import rmtree
    rmtree('tmp', ignore_errors=True)
    mkdir('tmp')
