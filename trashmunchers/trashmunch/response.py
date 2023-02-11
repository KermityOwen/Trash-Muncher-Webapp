import requests


class TestApiResponse:
    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("Successfully fetched the data")
        else:
            print(f"Failure in data fetching. Status code: {response.status_code}")

    def __init__(self, api):
        self.get_data(api)


if __name__ == "__main__":
    api_call = TestApiResponse("http://localhost:8000/dummy")
