import httpx
from pathlib import Path
import hashlib

from pydantic import BaseModel

from .sources import NpmVersion, EcoVersion, VersionDocument

class FetchEntry(BaseModel):
    status: int
    body: str

class Fetch:
    # what is fetch doing?
    # fetching package history of a given package name for repository
    def __init__(self, client: httpx.Client | None):
        if client is None:
            self.client = httpx.Client()
        else:
            self.client = client

    # fetches and stores a raw json in cache dir
    def get_json(self, url: str) -> FetchEntry | None:
        filename = hashlib.sha256(url.encode())
        p = Path("cache/" + filename.hexdigest())
        if p.exists():
            result = p.read_text()
            return FetchEntry.model_validate_json(result)
        else:
            response = self.client.get(url)
            if response.status_code == 200 or response.status_code == 404:
                f = FetchEntry(status = response.status_code, body = response.text)
                p.write_text(f.model_dump_json())
                return f
            else:
                response.raise_for_status()

    # fetch information from npm registory for a specific package
    # https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages/axios/versions/1.14.1
    def get_version(self, package: str, version: str) -> VersionDocument | None:
        url = "https://registry.npmjs.org" + f"/{package}/{version}"
        entry = self.get_json(url)
        # this entry should be a package document for the given package and version
        if entry.status == 200:
            document = NpmVersion.model_validate_json(entry.body)
            vd = VersionDocument(npm_user = document.npm_user, gitHead = document.gitHead)
        elif entry.status == 404:
            print("couldn't find it in npm, trying ecosystem.ms")
            url = "https://packages.ecosyste.ms/api/v1" + f"/registries/npmjs.org/packages/{package}/versions/{version}"
            entry = self.get_json(url)
            if entry.status == 200:
                document = EcoVersion.model_validate_json(entry.body)
                vd = VersionDocument(npm_user = document.metadata.npm_user, gitHead = document.metadata.gitHead)
            else:
                vd = None
        else:
            vd = None

        return vd
