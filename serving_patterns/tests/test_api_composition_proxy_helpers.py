import pytest
from src.api_composition_proxy import helpers


@pytest.mark.parametrize(
    ("url", "path", "expected"),
    [
        ("localhost", "aa", "localhost/aa"),
        ("localhost/", "aa", "localhost/aa"),
        ("localhost", "/aa", "localhost/aa"),
        ("localhost/", "/aa", "localhost/aa"),
        ("localhost", "", "localhost"),
        ("localhost", None, "localhost"),
    ],
)
def test_path_builder(url, path, expected):
    result = helpers.path_builder(url, path)
    assert result == expected


@pytest.mark.parametrize(
    ("hostname", "https", "expected"),
    [
        ("localhost", True, "https://localhost"),
        ("localhost", False, "http://localhost"),
        ("http://localhost", False, "http://localhost"),
        ("https://localhost", False, "https://localhost"),
    ],
)
def test_url_builder(hostname, https, expected):
    result = helpers.url_builder(hostname, https)
    assert result == expected


@pytest.mark.parametrize(
    ("hostname", "path", "https", "expected"),
    [
        ("localhost", "aa", True, "https://localhost/aa"),
        ("localhost/", "aa", False, "http://localhost/aa"),
        ("localhost", "/aa", False, "http://localhost/aa"),
        ("localhost/", "/aa", True, "https://localhost/aa"),
        ("localhost", "", True, "https://localhost"),
        ("localhost", None, False, "http://localhost"),
    ],
)
def test_url_path_builder(hostname, path, https, expected):
    result = helpers.url_path_builder(hostname, path, https)
    assert result == expected


@pytest.mark.parametrize(
    ("alias", "url", "redirect_path", "customized_redirect_map", "expected"),
    [
        ("SVC", "http://localhost/", "predict", {"SVC": {"predict": "predict/label"}}, "http://localhost/predict/label"),
        ("SVC", "http://localhost/", "apredict", {"SVC": {"predict": "predict/label"}}, "http://localhost/apredict"),
        ("ASVC", "http://localhost/", "apredict", {"SVC": {"predict": "predict/label"}}, "http://localhost/apredict"),
    ],
)
def test_customized_redirect_builder(alias, url, redirect_path, customized_redirect_map, expected):
    result = helpers.customized_redirect_builder(alias, url, redirect_path, customized_redirect_map)
    assert result == expected
