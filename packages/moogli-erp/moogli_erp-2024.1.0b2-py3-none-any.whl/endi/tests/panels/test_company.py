def test_get_page_number(get_csrf_request):
    from endi.panels.company_index.utils import get_page_number

    request = get_csrf_request(post={"page_nb": "5"})
    assert get_page_number(request, "page_nb") == 5
    assert get_page_number(request, "nutts") == 0


def test_make_get_list_url():
    from endi.panels.company_index.utils import make_get_list_url

    func = make_get_list_url("mylist")
    assert func(0) == "#mylist/0"
    assert func(5) == "#mylist/5"


def test_get_post_int(get_csrf_request):
    from endi.panels.company_index.utils import get_post_int

    request = get_csrf_request(post={"posted_int": "5"})
    assert get_post_int(request, "posted_int", 2) == 5
    assert get_post_int(request, "nutts", 2) == 2


def test_get_items_per_page(get_csrf_request):
    from endi.panels.company_index.utils import get_items_per_page

    default = 5

    request = get_csrf_request()
    assert get_items_per_page(request, "item_pp") == default
    request = get_csrf_request(cookies={"item_pp": "abc"})
    assert get_items_per_page(request, "item_pp") == default
    request = get_csrf_request(post={"item_pp": "abc"})
    assert get_items_per_page(request, "item_pp") == default

    request = get_csrf_request(post={"item_pp": 5})
    assert get_items_per_page(request, "item_pp") == 5

    request = get_csrf_request(post={"item_pp": "5"}, cookies={"item_pp": "10"})
    assert get_items_per_page(request, "item_pp") == 5

    request = get_csrf_request(cookies={"item_pp": "10"})
    assert get_items_per_page(request, "item_pp") == 10

    request = get_csrf_request(post={"item_pp": "abc"}, cookies={"item_pp": "10"})
    assert get_items_per_page(request, "item_pp") == 10
