import click
import PySimpleGUI as sg
import numpy as np
import io
import matplotlib.pyplot as plt
from PIL import Image


COLORMAP = [
    'plasma', 'viridis', 'inferno', 'magma', 'cividis',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral',
]

def update_image(
        data: np.ndarray,
        pixel_size: int,
        cmap: str = 'inferno',
    ) -> bytes:

    # Convert ndarray into image using matplotlib's imsave
    ibuf = io.BytesIO()
    plt.imsave(ibuf, data, cmap=cmap)

    # Convert png to PIL image to resize it
    img = Image.open(ibuf)
    img = img.resize([pixel_size*s for s in img.size])
    
    # Save PIL image to bytes, return bytes
    obuf = io.BytesIO()
    img.save(obuf, format='PNG')
    return obuf.getvalue()


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


def app(
        data: np.ndarray,
        name: str = 'Data Raster',
        pixel_size: int = 1,
        color_map: str = COLORMAP[0],
    ) -> None:
    
    img_elem = sg.Image(update_image(data, pixel_size, cmap=color_map), key='-IMAGE-')
    img_column = sg.Column(
        [[img_elem]],
        scrollable=True,
        expand_x=True,
        expand_y=True,
    )

    menu_def = [
        ['&File', ['&Save', '&Close']],
        ['&Color', COLORMAP],
    ]

    layout = [
        [
            sg.Menu(menu_def, key='-MENU-'),
        ],
        [
            sg.Text('Pixel Size'),
            sg.Spin([1,2,3,4,5], initial_value=pixel_size, key='-PIXELSIZE-', change_submits=True),
        ],
        [img_column],
        [sg.Button('Close', key='-CLOSE-')],
    ]

    window = sg.Window(
        name,
        layout,
        finalize=True,
        resizable=True,
    )

    window.TKroot.maxsize(*sg.Window.get_screen_size())

    while True:
        event, values = window.read()

        print(event, values)

        if event in (sg.WIN_CLOSED, 'Close'):
            break

        elif event == '-PIXELSIZE-':
            pixel_size = values['-PIXELSIZE-']

        elif event in COLORMAP:
            color_map = event

        img_elem.update(data=update_image(data, pixel_size, cmap=color_map))
        img_column.set_size([int(s*pixel_size+40) for s in img_column.get_size()])
        img_column.contents_changed()

    window.close()


@click.command()
@click.option('-p', '--pixel-size', type=click.Choice([str(x) for x in [1,2,3,4,5]]), default='1')
@click.option('-c', '--color-map', type=click.Choice(COLORMAP), default=COLORMAP[0])
def cli(pixel_size, color_map):
    pixel_size = int(pixel_size)
    data = generate_vertical_data((256*4, 512))
    app(data, 'numpy', pixel_size, color_map)
