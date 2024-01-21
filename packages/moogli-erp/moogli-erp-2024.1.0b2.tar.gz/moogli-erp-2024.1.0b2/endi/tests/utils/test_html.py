"""
Test for the forms package
"""
import colander
from endi.utils.html import (
    strip_whitespace,
    strip_linebreaks,
    strip_void_lines,
    clean_html,
    split_rich_text_in_blocks,
)


def test_strip_whitespace():
    value = "toto"
    assert strip_whitespace(value) == value
    value = "     toto\t   "
    assert strip_whitespace(value) == "toto"
    value = "   to    toto \t toto"
    assert strip_whitespace(value) == "to    toto \t toto"
    assert strip_whitespace(None) is None
    assert strip_whitespace(colander.null) == colander.null


def test_strip_linebreaks():
    value = "\n toto \n <br /><br><br/>"
    assert strip_linebreaks(value) == "toto"
    assert strip_linebreaks(None) is None
    assert strip_linebreaks(colander.null) == colander.null


def test_strip_void_lines():
    value = "<div></div><p>toto</p><p> </p>"
    assert strip_void_lines(value) == "<div></div><p>toto</p>"


def test_clean_html():
    value = "<span style=\"font-family: 'AGaramondPro'; display:none;\">Test</span>"

    assert (
        clean_html(value) == "<span style=\"font-family: 'AGaramondPro'\">Test</span>"
    )


def test_split_rich_text_in_blocks():
    res = split_rich_text_in_blocks("Facture d'acompte")
    assert res == ["Facture d'acompte"]
    res = split_rich_text_in_blocks("<ul><li>1</li><li>2</li></ul><p>3</p>")
    assert res == ["<ul><li>1</li><li>2</li></ul>", "<p>3</p>"]
    res = split_rich_text_in_blocks("<ul><li>1</li><li>2</li></ul>")
    assert res == ["<ul><li>1</li><li>2</li></ul>"]
    res = split_rich_text_in_blocks(
        "<div>Texte1<ul><li>1</li><li>2</li></ul>Texte2</div>"
    )
    assert res == ["<div>Texte1<ul><li>1</li><li>2</li></ul>Texte2</div>"]
    res = split_rich_text_in_blocks("<p>Texte1</p><ul><li>1</li><li>2</li></ul>Texte2")
    assert res == ["<p>Texte1</p>", "<ul><li>1</li><li>2</li></ul>Texte2"]

    s = """<p>- Cables et kit d'installation en inox (serres cables, embouts chapes, pontets )</p>
<ul>
<li>Cables : 40 m</li>
<li>Serres cables : x 32</li>
<li>Embouts chapes : x 32</li>
<li>Pontets : x 10</li>
</ul>"""
    assert split_rich_text_in_blocks(s) == [
        "<p>- Cables et kit d'installation en inox (serres cables, embouts chapes,"
        " pontets )</p>\n",
        """<ul>
<li>Cables : 40 m</li>
<li>Serres cables : x 32</li>
<li>Embouts chapes : x 32</li>
<li>Pontets : x 10</li>
</ul>""",
    ]
