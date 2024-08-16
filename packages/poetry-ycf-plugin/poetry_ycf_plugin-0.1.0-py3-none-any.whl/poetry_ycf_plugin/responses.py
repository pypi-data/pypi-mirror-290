from datetime import datetime

from pydantic import BaseModel


class StaticKeyAccessResponse(BaseModel):
    id: str
    serviceAccountId: str
    createdAt: str
    description: str
    keyId: str
    lastUsedAt: datetime | None = None


class StaticKeyResponse(BaseModel):
    accessKey: StaticKeyAccessResponse
    secret: str


class IamTokenResponse(BaseModel):
    iamToken: str
    expiresAt: datetime
