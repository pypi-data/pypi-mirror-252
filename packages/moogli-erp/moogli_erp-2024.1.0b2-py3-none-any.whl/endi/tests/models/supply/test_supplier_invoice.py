def test_supplier_invoice_duplicate(
    dbsession,
    half_cae_supplier_invoice,
):
    si = half_cae_supplier_invoice
    si2 = si.duplicate()
    dbsession.add(si2)
    dbsession.flush()

    assert len(si2.lines) == 2
    assert si2.lines[0].id != si.lines[0]

    assert si2.lines[0].description == si.lines[0].description
    assert si2.lines[0].ht == si.lines[0].ht
    assert si2.lines[0].tva == si.lines[0].tva
    assert si2.lines[0].type_id == si.lines[0].type_id
    assert si2.lines[0].business_id == si.lines[0].business_id

    assert si2.cae_percentage == si.cae_percentage
    assert si2.payer == si.payer
