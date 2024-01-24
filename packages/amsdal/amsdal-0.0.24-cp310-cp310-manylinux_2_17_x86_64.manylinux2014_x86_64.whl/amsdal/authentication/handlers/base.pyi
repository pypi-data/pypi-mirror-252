import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod

JWT_PUBLIC_KEY: str
ENCRYPT_PUBLIC_KEY: str
SYNC_KEY: bytes
BASE_AUTH_URL: Incomplete

class AuthHandlerBase(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def validate_credentials(self) -> None: ...
