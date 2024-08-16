import os.path

from dc_converter.convert import write_color_images, write_multi_view


def test_color():
    write_color_images(os.path.expanduser(
        './data/data.raw'))

def test_multi():
    write_multi_view(os.path.expanduser(
        './data/data.raw'),
        './data/multi_r.png')
