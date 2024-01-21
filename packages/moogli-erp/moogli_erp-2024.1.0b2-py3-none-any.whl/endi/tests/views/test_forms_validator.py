import unittest
import colander
from endi.forms.validators import validate_image_mime


class ValidatorsTest(unittest.TestCase):
    def test_validate_image_mime(self):
        form_datas = {"mimetype": "application/pdf", "filename": "file.pdf", "size": -1}
        self.assertRaises(colander.Invalid, validate_image_mime, "nutt", form_datas)
        form_datas = {"mimetype": "image/png", "filename": "file.png", "size": -1}
        self.assertEqual(None, validate_image_mime("nutt", form_datas))
