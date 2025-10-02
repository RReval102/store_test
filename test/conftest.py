import os
import pytest

from utils.api_client import PetStoreClient


@pytest.fixture(scope="session")
def base_url() -> str:
    
    return os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")


@pytest.fixture(scope="session")
def client(base_url: str) -> PetStoreClient:
    
    return PetStoreClient(base_url=base_url)