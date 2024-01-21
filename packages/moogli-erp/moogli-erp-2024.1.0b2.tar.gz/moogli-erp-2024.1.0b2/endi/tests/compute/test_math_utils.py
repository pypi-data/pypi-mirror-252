import unittest
import pytest

from endi.compute.math_utils import (
    floor_to_precision,
    floor,
    amount,
    percent,
    percentage,
    convert_to_int,
    compute_floored_ht_from_ttc,
    compute_genuine_ht_from_ttc,
    compute_ht_from_ttc_in_int,
    compute_ht_from_ttc,
    compute_tva,
    compute_tva_from_ttc,
    str_to_float,
    convert_to_float,
)


class TestMathUtils(unittest.TestCase):
    def test_floor(self):
        # Ref #727
        a = 292.65 * 100.0
        self.assertEqual(floor(a), 29265)
        a = 29264.91
        self.assertEqual(floor(a), 29265)
        self.assertEqual(floor(a, round_floor=True), 29264)
        a = 29264.5
        self.assertEqual(floor(a), 29265)

    def test_floor_to_precision(self):
        a = 299999
        self.assertEqual(floor_to_precision(a), 300000)
        a = 299455
        self.assertEqual(floor_to_precision(a), 299000)
        a = 299999
        self.assertEqual(floor_to_precision(a, round_floor=True), 299000)

    def test_amount(self):
        # Ref #727
        a = 192.65
        self.assertEqual(amount(a), 19265)
        a = 192.6555
        self.assertEqual(amount(a), 19266)
        self.assertEqual(amount(a, 4), 1926555)
        self.assertEqual(amount(a, 5), 19265550)

    def test_percent(self):
        self.assertEqual(percent(30, 10), 300.0)
        self.assertEqual(percent(1, 3), 33.33)
        self.assertRaises(ZeroDivisionError, percent, 1, 0)
        self.assertEqual(percent(1, 0, 5), 5)

    def test_percentage(self):
        # Ref #32
        a = 0.25
        b = 10000
        self.assertEqual(percentage(a, b), 25)

    def test_convert_to_int(self):
        self.assertEqual(convert_to_int("25"), 25)
        self.assertEqual(convert_to_int("NOOK", 25), 25)
        self.assertEqual(convert_to_int("NOOK", 0), 0)
        assert convert_to_int("NOOK", default=None) is None
        self.assertRaises(ValueError, convert_to_int, "NOOK")


def test_compute_tva():
    assert compute_tva(10000, 2000) == 2000


def test_compute_ht_from_ttc():
    total_ttc = 1196.0
    tva_rate = 1960
    result = 1000
    assert compute_ht_from_ttc(total_ttc, tva_rate) == result

    total_ttc = 1200000
    tva_rate = 2000
    result = 1000000.0
    assert compute_ht_from_ttc(total_ttc, tva_rate, False) == result

    total_ttc = 1000.0
    tva_rate = 1960
    result = 836.12
    assert compute_ht_from_ttc(total_ttc, tva_rate) == result

    total_ttc = 600000000
    tva_rate = 2000
    result = 500000000
    assert compute_ht_from_ttc(total_ttc, tva_rate, float_format=False) == result

    total_ttc = 100000000
    tva_rate = 300
    real_world_result = 97087000
    not_rounded_result = 97087379
    assert compute_floored_ht_from_ttc(total_ttc, tva_rate) == real_world_result
    assert compute_genuine_ht_from_ttc(total_ttc, tva_rate) == not_rounded_result
    assert compute_ht_from_ttc_in_int(total_ttc, tva_rate) == real_world_result


def test_compute_tva_from_ttc():
    total_ttc = 1196.0
    tva_rate = 1960
    result = 196.0
    assert compute_tva_from_ttc(total_ttc, tva_rate) == result

    total_ttc = 1200000
    tva_rate = 2000
    result = 200000
    assert compute_tva_from_ttc(total_ttc, tva_rate, False) == result

    total_ttc = 1000.0
    tva_rate = 1960
    result = 163.88
    assert compute_tva_from_ttc(total_ttc, tva_rate) == result


def test_str_to_float():
    source = "a15de d,12"
    dest = 15.12
    assert str_to_float(source) == dest


def test_convert_to_float():
    source = "a15de d,12"
    dest = 15.12
    assert convert_to_float(source, default=0.0) == 0.0
    assert convert_to_float(source, default=None) == None
    with pytest.raises(ValueError):
        convert_to_float(source)
    source = "15.12"
    dest = 15.12
    assert convert_to_float(source) == dest
