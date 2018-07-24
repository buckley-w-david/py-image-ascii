import enum
import typing

from PIL import Image
from PIL import GifImagePlugin


class Quality(enum.Enum):
    LOW = enum.auto()
    MEDIUM = enum.auto()
    HIGH = enum.auto()
    SOURCE = enum.auto()


class Ramp(enum.Enum):
    STANDARD = enum.auto()
    CONDENSED = enum.auto()


QUALITY_RATIO = {
    Quality.LOW: 0.25,
    Quality.MEDIUM: 0.50,
    Quality.HIGH: 0.75,
    Quality.SOURCE: 1.00,
}


RAMP = {
    Ramp.STANDARD: "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    Ramp.CONDENSED: " .:-=+*#%@"[::-1],
}


def from_intensity(intensity: int, colour_ramp: str) -> str:
    relative = min(int((intensity / 255) * len(colour_ramp)), len(colour_ramp) - 1)
    return colour_ramp[relative]


def transform_image(
    image: Image,
    quality=Quality.SOURCE,
    ramp: typing.Union[Ramp, str] = RAMP[Ramp.CONDENSED],
) -> str:
    if isinstance(ramp, str):
        pass
    elif isinstance(ramp, Ramp):
        ramp = RAMP[ramp]
    else:
        raise ValueError("ramp must be `Ramp` enum or `str`")

    # Convert...
    # 1. Grayscale
    # 2. Squash to 0.5 times height (character height is about twice width)
    # 3. Convert to characters
    ratio = QUALITY_RATIO[quality]
    width, height = int(image.width * ratio), int(image.height * 0.5 * ratio)
    processed = image.convert("L").resize((width, height))
    result = [["" for _ in range(width)] for _ in range(height)]
    pix = processed.load()

    for y in range(height):
        for x in range(width):
            result[y][x] = from_intensity(pix[x, y], ramp)

    return "\n".join("".join(row) for row in result)


def transform_animation(image: Image, ramp) -> typing.Iterator[str]:
    if not image.is_animated:
        raise ValueError("Image must be an animated gif")

    frames = (image.seek(frame) for frame in range(image.n_frames))
    tmp = []

    for frame in frames:
        import pdb

        pdb.set_trace()
        result = transform_image(image, ramp=ramp)
        tmp.append(result)

    for frame in tmp:
        yield frame


def _handle_animation_mix(image: Image, ramp):
    if image.is_animated:
        return transform_animation(image, ramp)
    return transform_image(image, ramp)


IMAGE_FORMAT_MAP = {
    "JPEG": transform_image,
    "PNG": transform_image,
    "GIF": _handle_animation_mix,
}


def transform(image: Image, ramp) -> typing.Union[str, typing.Iterator[str]]:
    return IMAGE_FORMAT_MAP[image.format](image, ramp=ramp)
