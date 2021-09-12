import colorsys
from typing import Tuple
from functools import singledispatch

@singledispatch
def toHLS(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return colorsys.rgb_to_hls(min(rgb[0], 255) / 255.0, min(rgb[1], 255) / 255.0, min(rgb[2], 255) / 255.0)
    # return colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

@toHLS.register
def _(r: float, g: float, b: float) -> Tuple[float, float, float]:
    return toHLS((r, g, b))

@singledispatch
def toRGB(hls: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return tuple(map(lambda x: x * 255, colorsys.hls_to_rgb(min(hls[0], 1), min(hls[1], 1), min(hls[2], 1))))
    # return tuple(map(lambda x: x * 255, colorsys.hls_to_rgb(hls[0], hls[1], hls[2])))
    # return tuple(map(lambda x: x * 255, colorsys.hsv_to_rgb(hls[0], hls[1], hls[2])))

@toRGB.register
def _(h: float, l: float, s: float) -> Tuple[float, float, float]:
    return toRGB((h, l, s))