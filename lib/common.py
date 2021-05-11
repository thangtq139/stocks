import requests
import random
import time


def wrap_request_post(url, headers, cookies, data):
    return wrap_request("POST", url, headers, cookies, data)


def wrap_request_get(url, headers=None, cookies=None, data=None):
    return wrap_request("GET", url, headers, cookies, data)


def wrap_request(scheme, url, headers, cookies, data, retry=3, timeout=30):
    max_retry = retry
    while True:
        wait_time = random.randint(500, 1000)
        try:
            if scheme == "POST":
                response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=timeout)
            elif scheme == "GET":
                response = requests.get(url, headers=headers, cookies=cookies, params=data, timeout=timeout)
            else:
                response = None
            time.sleep(wait_time * 1.0 / 1000)
            return response
        except:
            retry -= 1
            if retry == 0:
                raise
            time.sleep((max_retry - retry) * wait_time * 1.0 / 1000)
