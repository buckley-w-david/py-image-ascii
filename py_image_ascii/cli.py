import sys
import typing
import click
from PIL import Image
from py_image_ascii import transform as image_transform


@click.group()
def main():
    pass


@main.command()
@click.argument("image", type=click.File("rb"))
@click.argument("ascii", type=click.File("w"), required=False, default=sys.stdout)
@click.option(
    "--preset-ramp", type=click.Choice([preset.name for preset in image_transform.Ramp])
)
@click.option("--ramp", type=str)
def transform(image, ascii, preset_ramp: str, ramp: str) -> None:
    ramp_option: typing.Union[str, image_transform.Ramp]
    if ramp and preset_ramp:
        raise Exception()  # Can't have both
    elif ramp:
        ramp_option = ramp
    elif preset_ramp:
        ramp_option = image_transform.Ramp[preset_ramp]
    else:
        ramp_option = image_transform.Ramp.CONDENSED

    im = Image.open(image)
    result = image_transform.transform(im, ramp_option)
    if isinstance(result, str):
        ascii.write(result)
    else:  # TODO: A better way of showing animated images in text
        for frame in result:
            ascii.write(frame)
