from endi.models.third_party.services.third_party import ThirdPartyService
from endi.tests.tools import Dummy


def test_format_name():
    a = Dummy(lastname=None)
    assert ThirdPartyService.format_name(a) == ""
    a = Dummy(firstname="firstname", lastname="lastname", civilite="monsieur")
    assert ThirdPartyService.format_name(a) == "M. lastname firstname"


def test_get_label():
    a = Dummy(type="internal", company_name="test")
    assert ThirdPartyService.get_label(a) == "test"
    a = Dummy(type="company", company_name="test")
    assert ThirdPartyService.get_label(a) == "test"
    a = Dummy(
        type="individual",
        company_name="test",
        firstname="firstname",
        lastname="lastname",
        civilite="monsieur",
    )
    assert ThirdPartyService.get_label(a) == "M. lastname firstname"


def test_get_address():
    a = Dummy(
        type="company",
        company_name="test",
        firstname="firstname",
        lastname="lastname",
        civilite="monsieur",
        address="1 rue vieille",
        additional_address="1er étage",
        zip_code="23200",
        city="Aubusson",
        country="Limousin",
    )
    assert ThirdPartyService.get_address(a) == (
        "test\nM. lastname firstname\n"
        "1 rue vieille\n1er étage\n23200 Aubusson\nLimousin"
    )
