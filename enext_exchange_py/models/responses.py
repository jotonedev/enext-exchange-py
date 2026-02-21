from dataclasses import dataclass

@dataclass(frozen=True)
class EncryptedResponse:
    ct: str
    s: str
    iv: str
