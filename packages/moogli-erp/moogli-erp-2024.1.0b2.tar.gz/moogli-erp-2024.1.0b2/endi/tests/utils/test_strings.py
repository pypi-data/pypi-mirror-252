import unittest
import locale
from endi.utils import strings


class TestIt(unittest.TestCase):
    def test_format_amount(self):
        a = 1525
        b = 1525.3
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        self.assertEqual(strings.format_amount(a), "15,25")
        self.assertEqual(strings.format_amount(a, trim=False), "15,25")

        self.assertEqual(strings.format_amount(b), "15,25")
        self.assertEqual(strings.format_amount(b, trim=False), "15,25")

        c = 210000
        self.assertEqual(strings.format_amount(c, grouping=False), "2100,00")
        self.assertEqual(strings.format_amount(c, grouping=True), "2&nbsp;100,00")

        c = 21000000.0
        self.assertEqual(strings.format_amount(c, trim=False, precision=5), "210,00")
        c = 21000004.0
        self.assertEqual(strings.format_amount(c, trim=False, precision=5), "210,00004")
        c = 21000040.0
        self.assertEqual(strings.format_amount(c, trim=False, precision=5), "210,0004")

        self.assertEqual(strings.format_amount(c, trim=True, precision=5), "210,00")
        c = 21012000.0
        self.assertEqual(strings.format_amount(c, trim=False, precision=5), "210,12")

        # With None input
        self.assertEqual(strings.format_amount(None), "")
        # REf https://framagit.org/endi/endi/-/issues/951
        self.assertEqual(
            strings.format_amount(1234567, trim=False, precision=5), "12,34567"
        )
        self.assertEqual(
            strings.format_amount(
                1234567, trim=False, precision=5, display_precision=2
            ),
            "12,35",
        )

    def test_format_name(self):
        self.assertEqual(strings.format_name(None, "LastName"), "LASTNAME ")
        self.assertEqual(strings.format_name("Firstname", None), " Firstname")

    def test_remove_kms_training_zeros(self):
        a = "12000"
        b = "14000,00"
        c = "16000,60"
        self.assertEqual(strings.remove_kms_training_zeros(a), "12000")
        self.assertEqual(strings.remove_kms_training_zeros(b), "14000")
        self.assertEqual(strings.remove_kms_training_zeros(c), "16000,60")


def test_format_float():
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    from endi.utils.strings import format_float

    assert format_float(1.256, precision=2) == "1,26"
    res = format_float(1265.254, precision=2, html=False)
    assert res == "1\u202f265,25" or res == "1 265,25"
    assert format_float(1265.254, precision=2) == "1&nbsp;265,25"
    assert format_float(1265.254, precision=2, grouping=False) == "1265,25"
    assert format_float(1.256, precision=None) == "1.256"
    assert (
        format_float(1.256, precision=2, wrap_decimals=True)
        == '1<span class="decimal-part">,26</span>'
    )


def test_remove_newlines():
    from endi.utils.strings import remove_newlines

    assert remove_newlines(None) == None
    assert remove_newlines("hey") == "hey"
    assert remove_newlines("") == ""
    assert remove_newlines("a\nb") == "a b"
    assert remove_newlines("a\r\nb") == "a b"


def test_is_hours():
    from endi.utils.strings import is_hours

    for string in ("heure", "heure(s)", "Heure", "HEURES"):
        assert is_hours(string)

    assert not is_hours("jours")
    assert not is_hours("hoeouoroeoso")
    assert not is_hours(None)


def test_human_readable_filesize():
    assert strings.human_readable_filesize(None) == "Inconnu"
    assert strings.human_readable_filesize(1048576) == "1.0 MB"
