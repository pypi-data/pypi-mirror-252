from endi.utils.files import (
    encode_path,
    decode_path,
    issubdir,
    filesizeformat,
)


def test_encode_decode():
    st = "$deù % ù$ùdeù % - /// //  \ \dekodok %spkoij  idje  ' kopk \""
    encoded = encode_path(st)
    assert decode_path(encoded) == st


def test_issubdir():
    assert issubdir("/root/foo", "/root/foo/bar")
    assert not issubdir("/root/foo", "/root/bar")
    assert not issubdir("/root/foo", "/root/../../foo/bar")


def test_filesizeformat():
    assert filesizeformat(1024, 0) == "1ko"
    assert filesizeformat(1024, 1) == "1.0ko"
    assert filesizeformat(1024 * 1024, 0) == "1Mo"
    assert filesizeformat(1024 * 1024, 1) == "1.0Mo"
