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


def get_angle(origin_xy: tuple, satellite_xy: tuple, degrees: bool=True) -> float:
    """
    :param origin_xy:
        a tuple of (x, y) coordinates for the object at the center
    :param satellite_xy:
        a tuple of (x, y) coordinates for the object
        whose angle from the center will be returned
    :param degrees:
        boolean, if true will return degrees, else radians
    :return: float
        an angle between 0 and 360 in degrees
    """
    x1, y1 = origin_xy
    x2, y2 = satellite_xy
    conversion = -((180 / m.pi) % 360)
    return m.atan2(y2 - y1, x2 - x1) * (conversion if degrees else 1)


def is_inside(point: tuple, bounds) -> bool:
    return (bounds.left <= point[0] <= bounds.right and
            bounds.bottom <= point[1] <= bounds.top)


def is_touching(obj1: object, obj2: object) -> bool:
    touches = []
    for bound in obj1.bounds:
        touches.append(is_inside(bound, obj2))
    return True in touches


def is_outside(obj1: object, obj2: object) -> bool:
    touches = []
    for bound in obj1.bounds:
        touches.append(is_inside(bound, obj2))
    return [True, True, True, True] != touches


def get_orbit(planet, satellite, ratio_from_center=0.5, track=True):
    """
    :param planet:
        the _Character object that will be orbited around
    :param satellite:
        the image object that will be in orbit
    :param ratio_from_center:
        the ratio of how far the satellite will orbit around
        the planet in terms of the planets size. Default = 0.5
        so the object will orbit at a distance of 1/2 the
        size of the planet from the planet's center.
        (approx right on the edge)
    :param track:
        this will ensure the satellite will follow the angle
        attribute of its planet Default = True,
        False will place the object at a stationary orbit
        on whatever the current angle is
    :return:
        tuple of the xy coordinates where the satellite will appear
    """
    if track:
        rotated_satellite = pg.transform.rotate(satellite, planet.angle)
        offset_x_sat_self, offset_y_sat_self = get_offset(satellite, rotated_satellite)
        offset_x_planet_sat, offset_y_planet_sat = get_offset(planet.image, satellite)
        orbit_x = (planet.w * ratio_from_center) * m.cos(-planet.angle * (m.pi / 180))
        orbit_y = (planet.h * ratio_from_center) * m.sin(-planet.angle * (m.pi / 180))
        pos = (planet.x + orbit_x + offset_x_sat_self + offset_x_planet_sat,
               planet.y + orbit_y + offset_y_sat_self + offset_y_planet_sat)
    else:  # lazy outcome, didn't really take the time to think through. May revisit
        rotated_satellite = satellite
        pos = planet.x + (planet.w * ratio_from_center) * m.cos(-planet.angle * (m.pi / 180))
    return rotated_satellite, pos



