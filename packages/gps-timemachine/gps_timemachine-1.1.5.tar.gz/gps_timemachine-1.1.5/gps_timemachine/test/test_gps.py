import datetime as dt

from gps_timemachine.gps import gps_to_utc, load_leap_seconds


def test_gps_to_utc_start():
    # GPS and UTC were the same
    d = dt.date(1981, 1, 6)
    gps_time = 0.0
    expected_dt = dt.datetime(1981, 1, 6, 0, 0, 0)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_early_years():
    # GPS should be ahead of UTC by 2 seconds
    d = dt.date(1982, 7, 2)
    gps_time = 0.0
    expected_dt = dt.datetime(1982, 7, 1, 23, 59, 58)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_middle_years():
    # GPS and UTC should differ by 13 seconds
    d = dt.date(2000, 1, 1)
    gps_time = 0.0
    expected_dt = dt.datetime(1999, 12, 31, 23, 59, 47)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_later_years():
    # GPS and UTC should differ by 18 seconds
    d = dt.date(2017, 1, 2)
    gps_time = 0.0
    expected_dt = dt.datetime(2017, 1, 1, 23, 59, 42)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_later_years_with_hms():
    # GPS and UTC should differ by 18 seconds
    d = dt.date(2017, 1, 2)
    gps_time = 123456.789
    expected_dt = dt.datetime(2017, 1, 2, 12, 34, 38, 789000)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_large_milliseconds_bug():
    # GPS and UTC should differ by 18 seconds
    d = dt.date(2017, 1, 2)
    gps_time = 123456.9996
    expected_dt = dt.datetime(2017, 1, 2, 12, 34, 39)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_gps_to_utc_large_milliseconds_rolls_to_next_day():
    # GPS and UTC were the same
    d = dt.date(1981, 1, 6)
    gps_time = 235959.9996
    expected_dt = dt.datetime(1981, 1, 7, 0, 0, 0)

    actual_dt = gps_to_utc(d, gps_time)

    assert expected_dt == actual_dt


def test_load_leap_seconds():
    leap_seconds = load_leap_seconds()
    expected = (dt.datetime(1983, 7, 1, 0, 0), 3.0)
    actual = leap_seconds[25]

    assert expected == actual
