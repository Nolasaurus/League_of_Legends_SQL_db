# conftest.py
import os
import pytest
from dotenv import load_dotenv

@pytest.fixture(autouse=True, scope='session')
def set_env_vars():
    load_dotenv(".env", verbose=True)
    # Ensure a dummy API key exists so API_Client() can be instantiated in
    # unit tests that mock the actual HTTP calls.
    os.environ.setdefault("RIOT_API_KEY", "test-key-placeholder")