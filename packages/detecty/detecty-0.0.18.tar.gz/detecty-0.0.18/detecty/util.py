from pathlib import Path

from PIL import Image, ImageDraw, ImageFile
from torch import Tensor
from torchvision.transforms.functional import (pad, resize, to_grayscale,
                                               to_tensor)

from detecty.bbox import BBox

ImageFile.LOAD_TRUNCATED_IMAGES = True

TARGET_SIZE = 256


def draw_bbox(img: Image.Image, *bboxs: BBox):
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    for color, bb in zip(colors, bboxs):
        draw.rectangle(
            (bb.x1, bb.y1, bb.x2, bb.y2),
            outline=color,
            width=1)

    return img


def to_grayscale_tensor(img: Image.Image):
    return to_tensor(to_grayscale(img))


def load_img(path: str | Path):
    return to_grayscale_tensor(Image.open(path))


def scale_target_size(img: Tensor, ratio: float):
    if ratio == 1:
        return img

    _, h, w = img.shape

    return resize(
        img,
        [round(h * ratio), round(w * ratio)],
        antialias=True)


def pad_square(img: Tensor):
    _, h, w = img.shape

    if h == w:
        return img

    if h > w:
        return pad(img, [0, 0, h-w, 0])

    return pad(img, [0, 0, 0, w-h])


def scale_pad_square(img: Tensor):
    _, h, w = img.shape
    ratio = TARGET_SIZE / max(h, w)

    img = scale_target_size(img, ratio)
    img = pad_square(img)

    assert img.shape == (
        1, TARGET_SIZE, TARGET_SIZE), f'Expected (1, {TARGET_SIZE}, {TARGET_SIZE}), got {img.shape}'

    return ratio, img


def clear_tmp():
    from os import mkdir
    from shutil import rmtree
    rmtree('tmp', ignore_errors=True)
    mkdir('tmp')
