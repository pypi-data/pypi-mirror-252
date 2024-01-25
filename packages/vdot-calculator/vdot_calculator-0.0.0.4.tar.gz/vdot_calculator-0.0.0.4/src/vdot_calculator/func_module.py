"""
vdot_calculator Module

This module provides functions for calculating VDOT (Volume of Oxygen)
values based on the original Jack Danniels Running Formula.
bibliografy:
https://www.letsrun.com/forum/flat_read.php?thread=3704747
https://www.letsrun.com/forum/flat_read.php?thread=4858970

Usage:
>>> import datetime
>>> import vdot_calculator as vdot
>>> time = datetime.time(minute=27, second=00)
>>> distance = 5000 # meters
>>> vdot.vdot_from_time_and_distance(time, distance)
34.96321966414413

>>> import datetime
>>> import vdot_calculator as vdot
>>> pace = datetime.time(minute=5, second=24)
>>> distance = 5000 # meters
>>> vdot.vdot_from_distance_and_pace(distance,pace)
34.96321966414413

>>> import datetime
>>> import vdot_calculator as vdot
>>> pace = datetime.time(minute=5, second=24)
>>> time = datetime.time(minute=27, second=00)
>>> vdot.vdot_from_time_and_pace(time,pace)
34.96321966414413
"""

import math
import datetime


def direct(time_minutes: float, total_distance: float) -> float:
    """
     Calculate the VO2max using the Daniels Method.

     Parameters:
     - time_minutes (float): The total running time in minutes.
     - total_distance (float): The total running distance in meters.

     Returns:
     - float: The calculated VO2max.
     """
    velocity = total_distance / time_minutes
    percent_max = 0.8 + 0.1894393 * math.e ** (-0.012778 * time_minutes) + \
        0.2989558 * math.e ** (-0.1932605 * time_minutes)
    vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity ** 2
    vo2max = vo2 / percent_max
    return vo2max


def vdot_from_distance_and_pace(distance: float, pace: datetime.time) -> float:
    """
    Calculate VDOT from distance and pace.

    Parameters:
    - distance (float): The distance value of the run in meters.
    - pace (datetime.time): The pace value of the run.

    Returns:
    - float: The calculated VDOT value.
    """

    pace = check_time(pace)
    distance = check_number(distance)
    pace_minutes = convert_to_minutes(pace)
    total_time = distance * pace_minutes / 1000  # transforms distance from
    # km to meters
    vdot = direct(total_time, distance)
    return vdot


def vdot_from_time_and_distance(time: datetime.time, distance: float) -> float:
    """
        Calculate VDOT from time and distance.

        Parameters:
        - time (datetime.time): The time value of the run.
        - distance (float): The distance value of the run in meters.

        Returns:
        - float: The calculated VDOT value.
        """
    time = check_time(time)
    distance = check_number(distance)
    time_minutes = convert_to_minutes(time)
    vdot = direct(time_minutes, distance)
    return vdot


def vdot_from_time_and_pace(time: datetime.time, pace: datetime.time) -> float:
    """
        Calculate VDOT from time and pace.

        Parameters:
        - time (datetime.time): The time value of the run.
        - pace (datetime.time): The pace value of the run.

        Returns:
        - float: The calculated VDOT value.
        """
    time = check_time(time)
    pace = check_time(pace)
    time_minutes = convert_to_minutes(time)
    pace_minutes = convert_to_minutes(pace)
    distance = time_minutes / pace_minutes * 1000
    v_dot = direct(time_minutes, distance)
    return v_dot


def convert_to_minutes(time: datetime.time) -> float:
    """
     Convert a time value to minutes.

     Parameters:
     - time (datetime.time): The time value to be converted.

     Returns:
     - float: The time value in minutes.
     """
    time_minutes = time.minute + time.second / 60 + time.hour * 60
    return time_minutes


def check_number(value) -> float:
    """
    Checks if the input value is numeric and returns it as a float.

    Parameters:
    - value: Numeric value to be checked and converted to float.

    Returns:
    - float: Converted numeric value.

    Raises:
    - TypeError: If the input is not numeric (neither int nor float).
    """
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except (ValueError, TypeError):
            pass

    raise TypeError(
            "The input should be of numeric type, either int or float.")


def check_time(value) -> datetime.time:
    """
     Checks if the input value is of type datetime.time.

     Parameters:
     - value: Value to be checked for its type.

     Returns:
     - datetime.time: If the input is of type datetime.time.

     Raises:
     - TypeError: If the input is not of type datetime.time.
     """
    if isinstance(value, datetime.time):
        return value
    raise TypeError(
        "The input should be type datetime.time")
