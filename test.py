import requests
import json

base_url = "http://localhost:5905"
# base_url = "https://reports.hydris.dev"

def get_page():
    r = requests.get(base_url)
    print(r.content)


def test_send_message():
    r = requests.post(base_url + "/message/", data={"project": "testing", "access_code": "20", "message": "send testing"})
    print(r.content)

def test_send_file():
    with open("dockerfile", "rb") as f:
        r = requests.post(base_url + "/file/", files={"file": ("dockerfile.test", f, None)}, 
                          data={"project": "testing", "access_code": "20"})
    print(r.content)

# get_page()
test_send_message()
test_send_file()