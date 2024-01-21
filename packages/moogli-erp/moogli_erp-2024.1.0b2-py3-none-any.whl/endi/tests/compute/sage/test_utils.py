from endi.compute.sage.utils import (
    fix_sage_ordering,
    _track_analytical_orphans,
    _with_orphans_inplace,
)


def test_fix_sage_ordering_track_analytical_orphans():
    g134 = {"type_": "G"}
    a1 = {"type_": "A", "_general_counterpart": g134}
    g2 = {"type_": "G"}
    a2 = {"type_": "A", "_general_counterpart": g2}
    a3 = {"type_": "A", "_general_counterpart": g134}
    a4 = {"type_": "A", "_general_counterpart": g134}

    out = list(_track_analytical_orphans([g134, a1, g2, a2, a3, a4]))
    assert out == [
        {
            "type_": "G",
            "_analytic_orphans": [
                {"type_": "A", "_general_counterpart": g134},
                {"type_": "A", "_general_counterpart": g134},
            ],
        },
        {"type_": "A", "_general_counterpart": g134},
        {"type_": "G"},
        {"type_": "A", "_general_counterpart": g2},
    ]


def test_fix_sage_ordering_with_orphans_inplace():
    assert list(
        _with_orphans_inplace(
            [
                {"type_": "G", "id": 1, "_analytic_orphans": [{"type_": "A", "id": 2}]},
                {"type_": "A", "id": 3},
            ]
        )
    ) == [
        {"type_": "G", "id": 1},
        {"type_": "A", "id": 3},
        {"type_": "A", "id": 2},
    ]


def test_fix_sage_ordering():
    # alltogether !
    g134 = {"type_": "G"}
    a1 = {"type_": "A", "_general_counterpart": g134}
    g2 = {"type_": "G"}
    a2 = {"type_": "A", "_general_counterpart": g2}
    a3 = {"type_": "A", "_general_counterpart": g134}
    a4 = {"type_": "A", "_general_counterpart": g134}

    assert list(fix_sage_ordering([])) == []
    assert list(fix_sage_ordering([g2, a2])) == [g2, a2]
    assert list(fix_sage_ordering([g134, a1, g2, a2, a3, a4])) == [
        g134,
        a1,
        a3,
        a4,
        g2,
        a2,
    ]

    # NB: this messy case might not occur in real-endi-life, but the function
    # can handle it
    assert list(fix_sage_ordering([a1, g134, g2, a3, a4, a2])) == [
        g134,
        a1,
        a3,
        a4,
        g2,
        a2,
    ]
