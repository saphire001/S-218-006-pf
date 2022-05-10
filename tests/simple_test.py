"""This tests text on the webpage"""

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200