import httpx
class Fetch:
    # what is fetch doing?
    # fetching package history of a given package name for repository
    def __init__(self):
        self.history = []

    # /GET/{package}/{version}
    def fetch_registry(self, package: str, version: str):
        base = "https://registry.npmjs.org"
        endpoint = f"/{package}/{version}"
        with httpx.Client() as client:
            client.get(endpoint)


    def fetch_eco():
        pass
