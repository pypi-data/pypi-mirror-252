"""
    Test image resizing
"""
import pytest
import os
from endi.tests.conftest import DATASDIR

from PIL import Image

from endi.utils.image import (
    ImageResizer,
    ImageRatio,
)


@pytest.fixture
def ratio():
    return ImageRatio(5, 1)


@pytest.fixture
def resizer():
    return ImageResizer(800, 200)


def test_ratio_not_affect_equal(ratio):
    with open(os.path.join(DATASDIR, "entete5_1.png"), "rb") as image:
        image2 = ratio.complete(image)
        assert Image.open(image2).size == Image.open(image).size


def test_ratio_not_affect_less(ratio):
    with open(os.path.join(DATASDIR, "entete10_1.png"), "rb") as image:
        image2 = ratio.complete(image)
        assert Image.open(image2).size == Image.open(image).size


def test_ratio(ratio):
    with open(os.path.join(DATASDIR, "entete2_1.png"), "rb") as image:
        image2 = ratio.complete(image)

    img_obj2 = Image.open(image2)
    width, height = img_obj2.size
    assert width / height == 5


def test_resize_width(resizer):
    with open(os.path.join(DATASDIR, "entete2_1.png"), "rb") as image:
        image2 = resizer.complete(image)

    assert Image.open(image2).size[0] == 400
    assert Image.open(image2).size[1] == 200


def test_resize_height(resizer):
    with open(os.path.join(DATASDIR, "entete5_1.png"), "rb") as image:
        image2 = resizer.complete(image)

    assert Image.open(image2).size[0] == 800
    assert Image.open(image2).size[1] == 160


def test_resize_cmyk_bug880(resizer):
    with open(os.path.join(DATASDIR, "cmyk.jpg"), "rb") as image:
        result = resizer.complete(image)

    assert Image.open(result).size[0] <= 200
    assert Image.open(result).mode == "RGB"
