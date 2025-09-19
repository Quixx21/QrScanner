import os
import requests

BASE_URL = "http://localhost:8000"


def test_decode_success():
    file_path = os.path.join(os.path.dirname(__file__), "samples/ticket2.jpg")
    with open(file_path, "rb") as f:
        files = {"file": f}
        resp = requests.post(f"{BASE_URL}/decode", files=files)

    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "parsed" in data["info"]
    assert data["info"]["parsed"]["from"] == "Bratislava hl."
    assert data["info"]["parsed"]["to"] == "Košice"


def test_decode_no_file():
    resp = requests.post(f"{BASE_URL}/decode")
    assert resp.status_code == 422
