import json

def test_VIP_content(client):
    active = True
    point_in_time = 7 # random choice
    url = "/v1/VIP/%s" % point_in_time

    while active:
        response = client.get(url)
        if response.status_code == 200:
            try:
                data = json.loads( response.data )
                assert "source" in data
                assert data["source"] == "vip-db"
                assert "gpsCoords" in data
                assert "lat" in data["gpsCoords"]
                assert "long" in data["gpsCoords"]
                assert type(data["gpsCoords"]["lat"]) is float
                assert type(data["gpsCoords"]["long"]) is float

            except Exception as e:
                assert False

            active = False

def test_current_time_content(client):
    url = "/v1/now"
    response = client.get(url)
    assert response.status_code == 200
    try:
        data = json.loads( response.data )
        assert "now" in data

    except Exception as e:
        assert False