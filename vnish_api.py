import requests


def get_summary(ip, api_key):
    url = f'http://{ip}/api/v1/summary'
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        summary_data = response.json()
        return summary_data
    else:
        error_message = response.json()['err']
        err = f"Internal server error: {error_message}"
        return err


def get_info(ip, api_key):
    url = f'http://{ip}/api/v1/info'
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        info_data = response.json()
        return info_data
    else:
        error_message = response.json()['err']
        err = f"Internal server error: {error_message}"
        return err


def send_setting(ip, api_key, sending_data):
    url = f"http://{ip}/api/v1/settings"
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    post_response = requests.post(url, headers=headers, json=sending_data)
    if post_response.status_code == 200:
        info_data = post_response.json()
        return info_data
    else:
        error_message = post_response.json()['err']
        err = f"Internal server error: {error_message}"
        return err


def find_miner(ip, api_key, sending_data):
    url = f"http://{ip}/api/v1/find-miner"
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    post_response = requests.post(url, headers=headers, json=sending_data)
    if post_response.status_code == 200:
        info_data = post_response.json()
        return info_data
    else:
        error_message = post_response.json()['err']
        err = f"Internal server error: {error_message}"
        return err


def get_current_preset(ip, api_key):
    url = f"http://{ip}/api/v1/perf-summary"

    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        presets = response.json()
        current = presets['current_preset']['name']
        current = int(current)
        return current
    else:
        error_message = response.json()['err']
        err = f"Internal server error: {error_message}"
        return err