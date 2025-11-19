from app import get_version


def test_version_exists():
    v = get_version()
    assert isinstance(v, str)
    assert len(v.split(".")) == 3
