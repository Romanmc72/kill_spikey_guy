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
    conversion = ((180 / m.pi) % 360)
    return m.atan2(y2 - y1, x2 - x1) * (-conversion if degrees else 1)


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


def get_distance(point_a: tuple, point_b: tuple) -> float:
    """
    :param point_a:
        x,y tuple representing the first object
    :param point_b:
        x,y tuple representing the second object
    :return:
        using the pythagorean theorem we get the distance
        ((x1 - x2)^2 + (y1 - y2)^2)^0.5
    """
    a = point_a[0] - point_b[0]
    b = point_a[1] - point_b[1]
    return (a ** 2 + b ** 2) ** 0.5


def is_facing(obj1: object, obj2: object, rng: float) -> bool:
    """
    :param obj1:
        takes a _Character object
    :param obj2:
        takes another _Character object
    :param rng:
        float in degrees (0-180] (not radians)
        will be added + and - to the first character's angle,
        so 180 would mean no matter what it would consider
        character 1 to be facing character 2
    :return:
        True or False
        whether or not the first character's angle attribute
        points in the direction of the second character's center within a range
    """
    angle = get_angle(obj1.center, obj2.center) % 360
    if 0 < rng < 180:

        return
    elif rng >= 180:
        return True
    elif rng == 0:
        return obj1.angle == angle
    else:
        raise Exception

