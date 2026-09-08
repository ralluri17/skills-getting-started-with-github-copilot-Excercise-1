"""Shared pytest fixtures for the FastAPI test suite."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # activities is mutated in place by the API, so snapshot/restore it around each test
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)
