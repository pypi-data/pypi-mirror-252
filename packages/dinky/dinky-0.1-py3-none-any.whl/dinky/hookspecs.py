import pluggy

from PIL import ImageDraw

from dinky.layouts.layout_configuration import Zone

hookspec = pluggy.HookspecMarker("dinky")

@hookspec
def dinky_draw_zone(zone: Zone) -> ImageDraw:
    """Take a zone and fill it.

    :param zone: the zone to draw on
    :return: a list of ingredients
    """