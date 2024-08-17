import random
from math import sqrt
from pathlib import Path

import numpy as np
from torch import Tensor
from torchvision.io import read_image, write_jpeg
from torchvision.transforms.functional import center_crop, resize
from torchvision.utils import make_grid
from tqdm import tqdm

from mozyq.fs import fs


class Grid:
    def __init__(self, imgs: list[Tensor], tile_size=64):
        self.grid_size = int(sqrt(len(imgs)))
        self.imgs = imgs
        self.tile_size = tile_size
        self.output_size = tile_size * self.grid_size

        assert self.grid_size ** 2 == len(imgs), \
            'number of images must be a perfect square'

    def build(self, zoom: float = 1.0):
        assert zoom >= 1.0, 'zoom must be greater than 1.0'

        tile_size = int(self.tile_size * zoom)
        grid = make_grid([
            resize(img, [tile_size, tile_size])
            for img in self.imgs],
            padding=0)

        return center_crop(grid, [self.output_size, self.output_size])


def rnd_grid(pool: Path, grid_size=8):
    sample = random.sample(
        list(pool.glob('*.jpg')),
        grid_size ** 2)

    imgs = [
        read_image(str(jpg))
        for jpg in sample]

    return Grid(imgs)


if __name__ == '__main__':
    grid = rnd_grid(fs.dataset / 'photos' / 'ALL')

    for zoom in tqdm(np.arange(1.0, 2.0, 1/60)):
        img = grid.build(zoom)
        write_jpeg(img, f'grid/{zoom:.2f}.jpg')

    print('done')
