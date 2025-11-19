import app


def test_version_read():
    v = app.get_version()
    assert isinstance(v, str)
    assert len(v) > 0


def test_index_route():
    client = app.app.test_client()
    res = client.get("/")
    data = res.get_json()

    assert res.status_code == 200
    assert data["status"] in ["ok", "pipeline-test"]
    assert isinstance(data["version"], str)
