from endi.models.user import UserDatas
from endi.utils import colanderalchemy


def test_colanderalchemy_utils():

    columns = colanderalchemy.get_model_columns_list(
        UserDatas, ["id", "situation_situation_id"]
    )
    assert columns[0].name == "user_id"
    assert columns[5].name == "coordonnees_lastname"

    assert (
        colanderalchemy.get_colanderalchemy_column_info(columns[1], "title")
        == "Antenne de rattachement"
    )

    sections = colanderalchemy.get_colanderalchemy_model_sections(UserDatas)
    assert "Coordonnées" in sections
    assert sections[0] == "Activité"

    section_columns = colanderalchemy.get_model_columns_by_colanderalchemy_section(
        UserDatas, "Coordonnées"
    )
    assert section_columns[1].name == "coordonnees_lastname"
