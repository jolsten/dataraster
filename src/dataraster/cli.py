import click
import numpy as np
from .app import COLORMAP, app, make_image


def _generate_random_data(size: tuple) -> np.ndarray:
    return np.random.choice(range(256), size)


def _generate_horizontal_data(size: tuple) -> np.ndarray:
    nrows, ncols = size
    row = np.arange(ncols).astype('uint8')
    data = np.array([row] * nrows).astype('uint8')
    return data


def _generate_vertical_data(size: tuple) -> np.ndarray:
    nrows, ncols = size
    row = np.arange(nrows).astype('uint8')
    data = np.array([row] * ncols).astype('uint8').transpose()
    return np.ascontiguousarray(data)


@click.command()
@click.option('-p', '--pixel-size', type=click.Choice([str(x) for x in [1,2,3,4,5]]), default='1')
@click.option('-c', '--color-map', type=click.Choice(COLORMAP), default=COLORMAP[0])
@click.option('-s', '--save', type=click.File('wb'), default=None)
@click.option('-T', '--test', type=click.Choice(['random', 'vertical', 'horizontal']), default=None)
def cli(pixel_size, color_map, save, test):
    pixel_size = int(pixel_size)

    if test is None:
        # TODO: Get data from STDIN
        data = _generate_random_data((256*4, 512))
    elif test == 'random':
        data = _generate_random_data((256*4, 512))
    elif test == 'vertical':
        data = _generate_vertical_data((256*4, 512))
    elif test == 'horizontal':
        data = _generate_horizontal_data((256*4, 512))

    if save is None:
        app(data, 'Data Raster', pixel_size, color_map)
    else:
        make_image(data, pixel_size, color_map)    
