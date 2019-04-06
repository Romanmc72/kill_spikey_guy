import pygame as pg
import math as m


def get_offset(original: object, changed: object) -> tuple:
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


def get_angle(origin_xy: tuple, satellite_xy: tuple) -> float:
    """
    :param origin_xy:
        a tuple of (x, y) coordinates for the object at the center
    :param satellite_xy:
        a tuple of (x, y) coordinates for the object
        whose angle from the center will be returned
    :return: float
        an angle between 0 and 360 in degrees
    """
    x1, y1 = origin_xy
    x2, y2 = satellite_xy
    return m.atan2(y2 - y1, x2 - x1)*(-180 / m.pi)


def is_inside(point: tuple, bounds) -> bool:
    return (point[0] <= bounds.right
            and point[0] >=bounds.left
            and point[1] <= bounds.top
            and point[1] >= bounds.bottom)


def is_touching(obj1: object, obj2: object) -> bool:
    touches = []
    for bound in obj1.bounds:
        touches.append(is_inside(bound, obj2))
    return True in touches
