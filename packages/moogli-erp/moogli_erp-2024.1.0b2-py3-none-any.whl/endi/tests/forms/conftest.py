import pytest


@pytest.fixture
def schema_node():
    import colander

    return colander.SchemaNode(colander.String())
