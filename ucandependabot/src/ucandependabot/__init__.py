from .fetch_service import Fetch
import httpx
def main() -> None:

    # fetch.fetch_registry("axios", "1.14.0")
    url = "https://registry.npmjs.org/axios"
    client = httpx.Client()
    fetch = Fetch(client)
    try:
        fetch.get_json(url)
        vd = fetch.get_version("axios", "1.14.1")
        print(f"here's the internal version document: {vd}")
    except Exception as e:
        print(e)
    finally:
        client.close()
