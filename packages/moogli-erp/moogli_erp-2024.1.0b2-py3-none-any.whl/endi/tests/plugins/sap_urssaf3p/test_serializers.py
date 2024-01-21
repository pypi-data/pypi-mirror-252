import colander
import pytest

from endi.plugins.sap_urssaf3p.serializers import (
    InputParticulierDTOSchema,
    fix_tva_rounding,
    InputLieuNaissancoDTOSchema,
    InputPrestationSchema,
)


@pytest.fixture
def mk_sap_task_line(date_20210101, mk_task_line, tva, mk_product):
    def _mk_sap_task_line(cost, quantity, date=None):
        return mk_task_line(
            cost=cost,
            tva=tva.value,
            product=mk_product(urssaf_code_nature="200"),
            quantity=quantity,
            unity="heure",
            date=date or date_20210101,
        )

    return _mk_sap_task_line


@pytest.fixture
def sap_task_line(mk_sap_task_line):
    # 5.01€HT TVA20%, x2
    return mk_sap_task_line(cost=501000, quantity=2)


@pytest.fixture
def sap_task_line2(date_20200101, mk_sap_task_line):
    # 5.01€HT TVA20%
    return mk_sap_task_line(cost=501000, quantity=1, date=date_20200101)


@pytest.fixture
def sap_invoice(
    date_20210101,
    dbsession,
    mk_invoice,
    sap_task_line,
    sap_task_line2,
    mk_task_line_group,
    sap_customer,
):
    inv = mk_invoice(
        official_number="INV_001", customer=sap_customer, date=date_20210101
    )
    inv.line_groups = [mk_task_line_group(lines=[sap_task_line, sap_task_line2])]
    dbsession.merge(inv)
    dbsession.flush()
    return inv


def test_serialize_input_prestation_schema(sap_task_line, invoice):
    from endi.models.config import Config
    from endi.plugins.sap_urssaf3p.serializers import InputPrestationSchema

    Config.set("cae_business_identification", "91281880900090")
    sap_task_line.task = invoice
    assert InputPrestationSchema().serialize_task_line(sap_task_line) == {
        "codeNature": "200",
        # "codeActivite": "30A001", Falcutatif/non implém
        "quantite": 2.0,
        "unite": "HEURE",
        "mntUnitaireTTC": 6.012,
        "mntPrestationTTC": 12.02,
        "mntPrestationHT": 10.02,
        "mntPrestationTVA": 2.0,
        # "dateDebutEmploi": "2022-02-01T16:40:00Z", Facultatif, non implém
        # "complement1" Facultatif/non implém
        "complement2": "SIR91281880900090",
    }


def test_fix_tva_rounding():
    # simplified cstruct, only fields used for the fix
    cstruct = {
        "numFactureTiers": "INV_001",
        "mntFactureHT": 15.03,
        "mntFactureTTC": 18.04,  # tva compute on sum(ht) is ok but Inconsistent with…
        "inputPrestations": [
            {
                "quantite": 2.0,
                "mntUnitaireTTC": 6.01,
                "mntPrestationTTC": 12.02,  # that…
                "mntPrestationHT": 10.02,
                "mntPrestationTVA": 2.00,
            },
            {
                "quantite": 1.0,
                "mntUnitaireTTC": 6.01,
                "mntPrestationTTC": 6.01,  # and that
                "mntPrestationHT": 5.01,
                "mntPrestationTVA": 1.0,
            },
        ],
    }
    fixed = fix_tva_rounding(cstruct)

    assert fixed == {
        "numFactureTiers": "INV_001",
        "mntFactureHT": 15.03,
        "mntFactureTTC": 18.04,  # untouched
        "inputPrestations": [
            {
                "quantite": 2.0,
                "mntUnitaireTTC": 6.015,  # fixed
                "mntPrestationTTC": 12.03,  # fixed
                "mntPrestationHT": 10.02,
                "mntPrestationTVA": 2.01,  # fixed
            },
            {
                "quantite": 1.0,
                "mntUnitaireTTC": 6.01,
                "mntPrestationTTC": 6.01,
                "mntPrestationHT": 5.01,
                "mntPrestationTVA": 1.0,
            },
        ],
    }


def test_fix_tva_rounding_does_not_add_decimals():
    # non regression of https://framagit.org/endi/endi/-/issues/3752
    # reproduce an actual regression case
    # simplified cstruct, only fields used for the fix
    cstruct = {
        "inputPrestations": [
            {
                "mntPrestationHT": 39.59,
                "mntPrestationTTC": 47.51,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.508,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.59,
                "mntPrestationTTC": 47.51,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.508,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
        ],
        "mntFactureHT": 197.92,
        "mntFactureTTC": 237.5,
        "numFactureTiers": "INV_001",
    }

    fixed = fix_tva_rounding(cstruct)

    assert fixed == {
        "inputPrestations": [
            {
                "mntPrestationHT": 39.59,  # untouched
                "mntPrestationTTC": 47.49,  # touched, yay, no extra decimal !
                "mntPrestationTVA": 7.9,  # touched
                "mntUnitaireTTC": 47.49,  # touched
                "quantite": 1.0,
            },
            {  # others untouched
                "mntPrestationHT": 39.59,
                "mntPrestationTTC": 47.51,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.508,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
            {
                "mntPrestationHT": 39.58,
                "mntPrestationTTC": 47.5,
                "mntPrestationTVA": 7.92,
                "mntUnitaireTTC": 47.496,
                "quantite": 1.0,
            },
        ],
        "mntFactureHT": 197.92,
        "mntFactureTTC": 237.5,
        "numFactureTiers": "INV_001",
    }


def test_serialize_input_prestation_schema_amount_match(mk_sap_task_line, invoice):
    # non regression https://framagit.org/endi/endi/-/issues/3751
    # 58.33€ HT x 5
    line = mk_sap_task_line(cost=5833000, quantity=5)
    line.task = invoice
    serialized = InputPrestationSchema().serialize_task_line(line)

    # 5 x 69.996 = 349.98
    assert serialized["mntPrestationTTC"] == 349.98
    assert serialized["quantite"] == 5
    # 3 decimals, because only 2 causes rounding error
    assert serialized["mntUnitaireTTC"] == 69.996


def test_serialize_input_demande_paiement_schema(
    dbsession,
    sap_invoice,
    sap_task_line,
    sap_task_line2,
):
    from endi.plugins.sap_urssaf3p.serializers import InputDemandePaiementSchema

    # invoice.all_lines = [sap_task_line, sap_task_line2]

    sap_invoice.line_groups[0].lines = [sap_task_line, sap_task_line2]
    dbsession.merge(sap_invoice.line_groups[0])
    dbsession.merge(sap_invoice)
    dbsession.flush()
    # invoice.cache_totals()

    serialized = InputDemandePaiementSchema().serialize_invoice(sap_invoice)

    # Basic check on lines, see test_serialize_input_prestation_schema for more
    assert len(serialized["inputPrestations"]) == 2
    assert serialized["inputPrestations"][0]["unite"] == "HEURE"
    assert serialized["inputPrestations"][0]["mntPrestationHT"] == 10.02

    serialized["inputPrestations"] = []

    assert serialized == {
        "dateDebutEmploi": "2020-01-01T00:00:00Z",
        "dateFacture": "2021-01-01T00:00:00Z",
        "dateFinEmploi": "2021-01-01T00:00:00Z",
        "dateNaissanceClient": "1990-01-01T00:00:00Z",
        "idClient": "6a56a628-b09e-8707-787e-10f218a2d550",
        "idTiersFacturation": "enDI",
        "inputPrestations": [],  # See above
        "mntFactureHT": 15.03,
        "mntFactureTTC": 18.04,
        "numFactureTiers": "INV_001",
    }


def test_serialize_input_particulier_dto_schema(sap_customer):
    assert InputParticulierDTOSchema().serialize_customer(sap_customer) == {
        "adresseMail": "jeanne.durand@contact.fr",
        "adressePostale": {
            "codeCommune": "26220",
            "codePays": "99100",
            "codePostal": "26110",
            "codeTypeVoie": "R",
            "complement": "Batiment A",
            "libelleVoie": "du soleil",
            "lieuDit": colander.null,
            "libelleCommune": "Nyons",
            "numeroVoie": "",
            "lettreVoie": "",
        },
        "civilite": "1",
        "coordonneeBancaire": {
            "bic": "BNPAFRPP",
            "iban": "FR7630004000031234567890143",
            "titulaire": "Jean Dupont",
        },
        "dateNaissance": "1990-01-01T00:00:00Z",
        "lieuNaissance": {
            "codePaysNaissance": "99100",
            "communeNaissance": {"codeCommune": "288", "libelleCommune": "Meulun"},
            "departementNaissance": "077",
        },
        "nomNaissance": "Dupont",
        "nomUsage": "Durand",
        "numeroTelephonePortable": "0605040302",
        "prenoms": "Eric-Antoine Jean alain",
    }


def test_input_lieu_naissance(mk_urssaf_customer_data, customer):
    meulun_data = InputLieuNaissancoDTOSchema().serialize_sap_customer_data(
        mk_urssaf_customer_data(birthplace_city_code="77288", customer=customer)
    )
    assert meulun_data["communeNaissance"]["codeCommune"] == "288"
    assert meulun_data["departementNaissance"] == "077"

    corse_data = InputLieuNaissancoDTOSchema().serialize_sap_customer_data(
        mk_urssaf_customer_data(birthplace_city_code="2A004", customer=customer)
    )
    assert corse_data["communeNaissance"]["codeCommune"] == "004"
    assert corse_data["departementNaissance"] == "02A"

    # COM is the same case.
    dom_data = InputLieuNaissancoDTOSchema().serialize_sap_customer_data(
        # Fort-de-France
        mk_urssaf_customer_data(birthplace_city_code="97209", customer=customer)
    )
    assert dom_data["communeNaissance"]["codeCommune"] == "009"
    assert dom_data["departementNaissance"] == "972"

    ghana_data = InputLieuNaissancoDTOSchema().serialize_sap_customer_data(
        mk_urssaf_customer_data(
            customer=customer,
            birthplace_city="NOTINFRA",
            # This is how the UI fills the data if not in France:
            birthplace_department_code="",
            birthplace_city_code="",
            birthplace_country_code="99329",  # GHANA
        )
    )
    assert ghana_data == {
        "codePaysNaissance": "99329",
    }
