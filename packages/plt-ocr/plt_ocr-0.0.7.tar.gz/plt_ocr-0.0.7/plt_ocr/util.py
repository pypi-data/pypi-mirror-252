from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFile
from torch import Tensor
from torchvision.transforms.functional import resize, to_grayscale, to_tensor

ImageFile.LOAD_TRUNCATED_IMAGES = True


def to_grayscale_tensor(img: Image.Image):
    return to_tensor(to_grayscale(img))


def load_img(path: str | Path):
    return to_grayscale_tensor(Image.open(path))


def pad_resize(img: Tensor, target_height=128, target_width=256):
    _, h, w = img.shape
    aspect = w / h
    target_aspect = target_width / target_height

    if aspect < target_aspect:
        img = resize(
            img,
            [target_height, int(target_height * aspect)],
            antialias=True)

    if aspect > target_aspect:
        img = resize(
            img,
            [int(target_width / aspect), target_width],
            antialias=True)

    _, h, w = img.shape

    res = torch.zeros((1, target_height, target_width))
    res[:, :h, :w] = img

    return res


def clear_tmp():
    from os import mkdir
    from shutil import rmtree
    rmtree('tmp', ignore_errors=True)
    mkdir('tmp')
