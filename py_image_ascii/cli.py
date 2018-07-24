import sys
import click
from PIL import Image
from py_image_ascii import transform as image_transform


@click.group()
def main():
    pass


@main.command()
@click.argument("image", type=click.File("rb"))
@click.argument("ascii", type=click.File("w"), required=False, default=sys.stdout)
def transform(image, ascii) -> None:
    im = Image.open(image)
    result = image_transform.transform(im)
    if isinstance(result, str):
        ascii.write(result)
    else:  # TODO: A better way of showing animated images in text
        for frame in result:
            ascii.write(frame)
