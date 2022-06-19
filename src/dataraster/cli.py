import click
import numpy as np
from .app import COLORMAP, app

def generate_random_data(size: tuple) -> np.ndarray:
    return np.random.choice(range(256), size)


def generate_horizontal_data(size: tuple) -> np.ndarray:
    nrows, ncols = size
    row = np.arange(ncols).astype('uint8')
    data = np.array([row] * nrows).astype('uint8')
    return data


def generate_vertical_data(size: tuple) -> np.ndarray:
    nrows, ncols = size
    row = np.arange(nrows).astype('uint8')
    data = np.array([row] * ncols).astype('uint8').transpose()
    return np.ascontiguousarray(data)


@click.command()
@click.option('-p', '--pixel-size', type=click.Choice([str(x) for x in [1,2,3,4,5]]), default='1')
@click.option('-c', '--color-map', type=click.Choice(COLORMAP), default=COLORMAP[0])
def cli(pixel_size, color_map):
    pixel_size = int(pixel_size)
    data = generate_vertical_data((256*4, 512))
    app(data, 'numpy', pixel_size, color_map)
