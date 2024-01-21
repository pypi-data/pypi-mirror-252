import colander
from endi.views import BaseRestView
from endi.tests.tools import Dummy


class Person(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    age = colander.SchemaNode(colander.Int())


class MyView(BaseRestView):
    schema = Person()


def test_base_rest_view_ref2486():
    """
    https://framagit.org/endi/endi/-/issues/2486
    """
    request = Dummy(context="", dbsession="", session="")
    view = MyView(request)
    schema = view.get_schema({})
    res_schema = view._filter_edition_schema(schema, {"name": "test"})
    assert len(res_schema.children) == 1

    # New request on veut le schéma d'origine, pas la version filtrée à l'étape
    # précédente
    view = MyView(request)
    schema = view.get_schema({})
    assert len(schema.children) == 2
