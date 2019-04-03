import pygame as pg


def get_offset(original, changed):
    """
    :param original:
        The original must be a pygame surface,
        and it will be the object whose center
        is the reference point for the offset
    :param changed:
        The changed pygame surface whose center
        will be aligned with the original
    :return:
        tuple of (x, y) coordinates by which the offset will occur
    """
    return ((original.get_width() / 2) - (changed.get_width() / 2),
            (original.get_height() / 2) - (changed.get_height() / 2))
