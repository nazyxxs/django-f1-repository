import requests

class NetworkHelper:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.auth = (username, password)

    def get_list(self, endpoint):
        url = f"{self.base_url}/{endpoint}/"
        response = requests.get(url, auth=self.auth)
        return response.status_code, response.json()

    def get_item(self, endpoint, item_id):
        url = f"{self.base_url}/{endpoint}/{item_id}/"
        response = requests.get(url, auth=self.auth)
        return response.status_code, response.json()

    def create_item(self, endpoint, data: dict):
        url = f"{self.base_url}/{endpoint}/"
        response = requests.post(url, json=data, auth=self.auth)
        return response.status_code, response.json()

    def update_item(self, endpoint, item_id, data: dict):
        url = f"{self.base_url}/{endpoint}/{item_id}/"
        response = requests.put(url, json=data, auth=self.auth)
        return response.status_code, response.json()

    def delete_item(self, endpoint, item_id):
        url = f"{self.base_url}/{endpoint}/{item_id}/"
        response = requests.delete(url, auth=self.auth)
        return response.status_code
