# Robaire Galliath, 2024

import pytest

from orbit.tle import TLE


def test_from_string_length():

    with pytest.raises(ValueError):
        TLE.from_string("")

    with pytest.raises(ValueError):
        TLE.from_string("1\n2\n3\n4")


def test_from_string_format():

    with pytest.raises(ValueError):
        TLE.from_string("BAD SAT\n1 3434N 98032A\n2 FOO BAR")


def test_from_string_ISS():

    iss_tle_str = """ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    iss_tle = TLE.from_string(iss_tle_str)

    assert iss_tle.title == "ISS (ZARYA)"
    assert iss_tle.catalog_number == 25544
    assert iss_tle.classification == "U"
    assert iss_tle.launch_year == 98
    assert iss_tle.launch_number == 67
    assert iss_tle.launch_piece == "A"
    assert iss_tle.epoch_year == 8
    assert iss_tle.epoch_day == 264.51782528
    assert iss_tle.mean_motion_d1 == -0.00002182
    assert iss_tle.mean_motion_d2 == 0.0
    assert iss_tle.b_star == -0.11606e-4
    assert iss_tle.ephemeris_type == 0
    assert iss_tle.element_number == 292
    assert iss_tle.inclination == 51.6416
    assert iss_tle.right_ascension == 247.4627
    assert iss_tle.eccentricity == 0.0006703
    assert iss_tle.argument_perigee == 130.5360
    assert iss_tle.mean_anomaly == 325.0288
    assert iss_tle.mean_motion == 15.72125391
    assert iss_tle.revolutions_epoch == 56353


def test_from_string_two_line():

    iss_tle_str = """
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    iss_tle = TLE.from_string(iss_tle_str)

    assert iss_tle.title == ""
    assert iss_tle.catalog_number == 25544
    assert iss_tle.classification == "U"
    assert iss_tle.launch_year == 98
    assert iss_tle.launch_number == 67
    assert iss_tle.launch_piece == "A"
    assert iss_tle.epoch_year == 8
    assert iss_tle.epoch_day == 264.51782528
    assert iss_tle.mean_motion_d1 == -0.00002182
    assert iss_tle.mean_motion_d2 == 0.0
    assert iss_tle.b_star == -0.11606e-4
    assert iss_tle.ephemeris_type == 0
    assert iss_tle.element_number == 292
    assert iss_tle.inclination == 51.6416
    assert iss_tle.right_ascension == 247.4627
    assert iss_tle.eccentricity == 0.0006703
    assert iss_tle.argument_perigee == 130.5360
    assert iss_tle.mean_anomaly == 325.0288
    assert iss_tle.mean_motion == 15.72125391
    assert iss_tle.revolutions_epoch == 56353


def test_from_file(fs):

    iss_tle_str = """ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    fs.create_file("iss_tle.txt", contents=iss_tle_str)

    iss_tle = TLE.from_file("iss_tle.txt")

    assert iss_tle.title == "ISS (ZARYA)"
    assert iss_tle.catalog_number == 25544
    assert iss_tle.classification == "U"
    assert iss_tle.launch_year == 98
    assert iss_tle.launch_number == 67
    assert iss_tle.launch_piece == "A"
    assert iss_tle.epoch_year == 8
    assert iss_tle.epoch_day == 264.51782528
    assert iss_tle.mean_motion_d1 == -0.00002182
    assert iss_tle.mean_motion_d2 == 0.0
    assert iss_tle.b_star == -0.11606e-4
    assert iss_tle.ephemeris_type == 0
    assert iss_tle.element_number == 292
    assert iss_tle.inclination == 51.6416
    assert iss_tle.right_ascension == 247.4627
    assert iss_tle.eccentricity == 0.0006703
    assert iss_tle.argument_perigee == 130.5360
    assert iss_tle.mean_anomaly == 325.0288
    assert iss_tle.mean_motion == 15.72125391
    assert iss_tle.revolutions_epoch == 56353
