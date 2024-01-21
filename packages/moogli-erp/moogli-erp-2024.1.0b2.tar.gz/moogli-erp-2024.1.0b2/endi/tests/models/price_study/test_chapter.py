def test_json_repr(mk_price_study_chapter, task_line_group):
    chapter = mk_price_study_chapter(
        description="Desc", title="Tit", order=1, task_line_group=task_line_group
    )
    dup = chapter.duplicate()
    assert dup.description == chapter.description
    assert dup.title == chapter.title
    assert dup.order == chapter.order
    assert dup.task_line_group is None


def test_sync_with_task(estimation, mk_price_study_chapter, get_csrf_request_with_db):
    request = get_csrf_request_with_db()
    estimation.line_groups = []
    request.dbsession.merge(estimation)
    chapter = mk_price_study_chapter(description="Desc", title="Tit", order=1)
    group = chapter.sync_with_task(request, estimation)

    assert group.task_id == estimation.id
    assert group.title == chapter.title
    assert group.description == chapter.description
    assert group.order == chapter.order
    assert chapter.task_line_group == group
    assert chapter.task_line_group_id == group.id
    group2 = chapter.sync_with_task(request, estimation)
    assert group == group2
