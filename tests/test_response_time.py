import time

VIP_url = "/v1/VIP/%s"

#common workhorse
def durationTest(client, times):
    point_in_time = 2 # random choice
    url = VIP_url % point_in_time
    start = 0
    end = 0

    for i in range(times):
        start = time.time()
        response = client.get(url)
        end = time.time()

        assert (end-start) < 5.0

def test_maximum_duration_short(client):
    durationTest(client, 10)

def test_maximum_duration_medium(client):
    durationTest(client, 100)

def test_maximum_duration_long(client):
    durationTest(client, 1000)