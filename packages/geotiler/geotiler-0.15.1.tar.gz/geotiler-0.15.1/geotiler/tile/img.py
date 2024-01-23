#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014 - 2024 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

"""
Render map image using map tile data.
"""

import io
import functools
import logging

import PIL.Image  # type: ignore
import PIL.ImageDraw  # type: ignore

logger = logging.getLogger(__name__)

async def render_image(map, tiles):
    """
    Redner map image using map tile data.

    Each item in tile data collection is tile image data, which can be
    interpreted with `PIL` library (via `PIL.Image.open` call, i.e. PNG
    file data or JPEG file data). The item can also be `None` if tile data
    could not be downloaded, i.e. due to network error.

    The map tiles are rendered into single map image. Error tile image is
    rendered if data for a tile does not exist.

    The PIL image object is returned.

    :param map: Map object.
    :param tiles: Asynchronous generator of map tiles.
    """
    if __debug__:
        logger.debug('combining tiles')

    provider = map.provider

    # PIL requires image size to be a tuple
    image = PIL.Image.new('RGBA', tuple(map.size))
    error = _error_image(provider.tile_width, provider.tile_height)

    async for tile in tiles:
        img = _tile_image(tile.img) if tile.img else error
        image.paste(img, tile.offset)

    return image

@functools.lru_cache(maxsize=4)
def _error_image(width, height):
    """
    Create error tile image.

    The error tile image is PIL image object showing message that a map
    tile could not be downloaded.

    :param width: Width of tile image.
    :param height: Height of tile image.
    """
    img = PIL.Image.new('RGBA', (width, height))
    draw = PIL.ImageDraw.Draw(img)
    msg = 'Error downloading map tile.'
    x0 = width / 2
    y0 = height / 2
    bb_l, bb_t, bb_r, bb_b = draw.textbbox((int(x0), int(y0)), msg)
    x = x0 + (bb_r - bb_l) / 2
    y = y0 + (bb_b - bb_t) / 2
    draw.text((int(x), int(y)), msg, 'red')
    return img

def _tile_image(data):
    """
    Convert image data like PNG file data or JPEG file data into
    `PIL.Image` object.

    :param data: Tile data, i.e. PNG file data.
    """
    f = io.BytesIO(data)
    return PIL.Image.open(f).convert('RGBA')


# vim: sw=4:et:ai
