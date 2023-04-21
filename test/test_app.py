def test_app(client):

    res = client.get('/')
    assert res.status_code == 200

def test_simple():
    assert 1 == 1