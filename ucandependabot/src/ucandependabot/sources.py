"""Raw response shapes for each data source (npm, ecosyste.ms)"""

from datetime import datetime

from pydantic import BaseModel, Field

class TrustedPublisher(BaseModel):
    id: str  # e.g. "github"
    oidcConfigId: str | None = None


class NpmUser(BaseModel):
    name: str
    email: str | None = None
    # Present only when published via OIDC trusted publishing (CI), not a personal token.
    trustedPublisher: TrustedPublisher | None = None


class Provenance(BaseModel):
    predicateType: str


class Attestations(BaseModel):
    url: str
    provenance: Provenance | None = None


class Signature(BaseModel):
    keyid: str
    sig: str


class Dist(BaseModel):
    shasum: str
    tarball: str
    integrity: str | None = None
    attestations: Attestations | None = None
    signatures: list[Signature] = []
    fileCount: int | None = None
    unpackedSize: int | None = None


class NpmDocFields(BaseModel):
    """Fields of npm's per-version document. ecosyste.ms copies these into `metadata`."""

    npm_user: NpmUser | None = Field(default=None, alias="_npmUser")
    gitHead: str | None = None
    dist: Dist
    scripts: dict[str, str] = {}


class NpmVersion(NpmDocFields):
    """GET https://registry.npmjs.org/{pkg}/{version}

    No publish timestamp here; npm only has it in the full packument's `time` map.
    """

    name: str
    version: str
    dependencies: dict[str, str] = {}  # runtime deps only: {name: range}


class EcoDependency(BaseModel):
    package_name: str
    requirements: str
    kind: str  # "runtime", "Development", ...
    optional: bool = False


class EcoVersion(BaseModel):
    """GET https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages/{pkg}/versions/{version}

    `metadata` has no name, version or dependencies; those live at the top level.
    """

    number: str
    published_at: datetime
    metadata: NpmDocFields
    dependencies: list[EcoDependency] = []  # includes dev deps; filter on `kind`


class VersionDocument(BaseModel):
    npm_user: NpmUser | None
    gitHead: str | None = None
