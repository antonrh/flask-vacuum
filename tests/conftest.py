import pytest
from flask import Flask


@pytest.fixture()
def dummy_app():
    app = Flask("dummy")
    app.debug = True
    return app
