import PySimpleGUI as sg
import numpy as np
from numpy.typing import ArrayLike
import io
import matplotlib.pyplot as plt
from PIL import Image


MAX_PIXEL_SIZE = 5
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


def app(
        data: ArrayLike,
        name: str = 'Data Raster',
        pixel_size: int = 1,
        color_map: str = COLORMAP[0],
    ) -> None:

    data = np.asarray(data)
    
    img_elem = sg.Image(update_image(data, pixel_size, cmap=color_map), key='-IMAGE-')
    img_column = sg.Column(
        [[img_elem]],
        scrollable=True,
        expand_x=True,
        expand_y=True,
    )

    menu_def = [
        ['&File', ['&Close::-CLOSE-']],
        ['&Color', [f'{c}::-COLORMAP-' for c in COLORMAP]],
    ]

    layout = [
        [
            sg.Menu(menu_def, key='-MENU-'),
        ],
        [
            sg.Text('Pixel Size'),
            sg.Spin(list(range(MAX_PIXEL_SIZE)), initial_value=pixel_size, key='-PIXELSIZE-', change_submits=True),
        ],
        [img_column],
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

        if event in (sg.WIN_CLOSED, 'Close::-CLOSE-'):
            break

        elif event == '-PIXELSIZE-':
            pixel_size = values['-PIXELSIZE-']

        elif '-COLORMAP-' in event:
            color_map = event.replace('::-COLORMAP-','')

        img_elem.update(data=update_image(data, pixel_size, cmap=color_map))
        img_column.set_size([int(s*pixel_size+40) for s in img_column.get_size()])
        img_column.contents_changed()

    window.close()
