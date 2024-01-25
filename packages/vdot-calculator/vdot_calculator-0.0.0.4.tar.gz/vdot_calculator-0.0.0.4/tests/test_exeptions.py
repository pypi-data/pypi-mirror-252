import src.vdot_calculator.func_module as vdot
import datetime
from pytest import mark
import pytest


@mark.type_error
def test_vdot_from_distance_and_pace_TYPE_ERROR_1():
    distance = 5000.0
    pace = 7
    with pytest.raises(TypeError) as excinfo:
        v_dot = vdot.vdot_from_distance_and_pace(distance, pace)
    assert str(excinfo.value) == "The input should be type datetime.time"


@mark.type_error
def test_vdot_from_distance_and_pace_TYPE_ERROR_2():
    distance = datetime.time(minute=5, second=7)
    pace = datetime.time(minute=5, second=7)
    with pytest.raises(TypeError) as excinfo:
        v_dot = vdot.vdot_from_distance_and_pace(distance, pace)
    assert str(excinfo.value) == "The input should be of numeric type, either int or float."


@mark.type_error
def test_vdot_from_distance_and_pace_TYPE_ERROR_3():
    distance = "jorginho"
    pace = datetime.time(minute=5, second=7)
    with pytest.raises(TypeError) as excinfo:
        v_dot = vdot.vdot_from_distance_and_pace(distance, pace)
    assert str(excinfo.value) == "The input should be of numeric type, either int or float."


@mark.xfail
def test_vdot_from_time_and_distance_TYPE_ERROR_1():
    distance = 5000.0
    time = datetime.time(minute=35, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be of numeric type, either int or float."


@mark.xfail
def test_vdot_from_time_and_distance_TYPE_ERROR_2():
    distance = "5000"
    time = datetime.time(minute=35, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be of numeric type, either int or float."

def test_vdot_from_time_and_distance_TYPE_ERROR_3():
    distance = "joãozinho"
    time = datetime.time(minute=35, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be of numeric type, either int or float."

def test_vdot_from_time_and_distance_TYPE_ERROR_4():
    distance = datetime.time(minute=35, second=0)
    time = datetime.time(minute=35, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be of numeric type, either int or float."

def test_vdot_from_time_and_distance_TYPE_ERROR_5():
    distance = 5000
    time = "35:00"
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"

def test_vdot_from_time_and_distance_TYPE_ERROR_6():
    distance = 5000
    time = 35
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_distance(time, distance)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"

@mark.xfail
def test_vdot_from_time_and_pace_TYPE_ERROR_1():
    time = datetime.time(minute=35, second=0)
    pace = datetime.time(minute=7, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_pace(time, pace)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"


def test_vdot_from_time_and_pace_TYPE_ERROR_2():
    time = 35
    pace = datetime.time(minute=7, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_pace(time, pace)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"

def test_vdot_from_time_and_pace_TYPE_ERROR_3():
    time = "35:00"
    pace = datetime.time(minute=7, second=0)
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_pace(time, pace)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"

def test_vdot_from_time_and_pace_TYPE_ERROR_4():
    time = datetime.time(minute=35, second=0)
    pace = 7
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_pace(time, pace)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"


def test_vdot_from_time_and_pace_TYPE_ERROR_5():
    time = datetime.time(minute=35, second=0)
    pace = "7:00"
    with pytest.raises(TypeError) as excinfo:
        vdot.vdot_from_time_and_pace(time, pace)
    assert str(excinfo.value) == \
           "The input should be type datetime.time"

