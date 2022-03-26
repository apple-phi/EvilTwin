import os
import shutil

from PIL import Image
import numpy as np


def rgb(hex_: str):
    hex_ = hex_.lstrip("#")
    return tuple(int(hex_[i : i + 2], 16) for i in (0, 2, 4))


translation = {
    "#f6e0c8": "#4cc9f0",
    "#EFAAA5": "#4895ef",
    "#E17CB7": "#3f37c9",  #
    "#BF53C9": "#a056ff",
    "#503197": "#480ca8",
    "#18215D": "#18215D",
}
translation = {rgb(k): rgb(v) for k, v in translation.items()}


def process(im):
    arr = np.array(im)
    out = arr.copy()
    for (r, g, b), v in translation.items():
        red, green, blue, alpha = arr.T
        selection = (red == r) & (green == g) & (blue == b)
        out[..., :-1][selection.T] = v
    return Image.fromarray(out)


def copy(path, dst):
    shutil.copy2(path, dst)
    im = Image.open(dst)
    process(im).save(dst)


shutil.copytree(
    "/Users/sandrachua/EvilTwin/EvilTwin/assets/sprites/player",
    "/Users/sandrachua/EvilTwin/EvilTwin/assets/sprites/enemy",
    copy_function=copy,
    dirs_exist_ok=True,
)
