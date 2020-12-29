from typing import Dict
import logging

logger = logging.getLogger(__name__)


def path_builder(url: str, path: str) -> str:
    if path == "" or path is None:
        return url
    if path.startswith("/"):
        path = path[1:]
    if url.endswith("/"):
        url = f"{url}{path}"
    else:
        url = f"{url}/{path}"
    return url


def url_builder(hostname: str, https: bool = False) -> str:
    if not (hostname.startswith("http://") or hostname.startswith("https://")):
        hostname = f"https://{hostname}" if https else f"http://{hostname}"
    return hostname


def url_path_builder(hostname: str, path: str, https: bool = False) -> str:
    hostname = url_builder(hostname, https)
    url = path_builder(hostname, path)
    return url


def customized_redirect_builder(alias: str, url: str, redirect_path: str, customized_redirect_map: Dict[str, Dict[str, str]] = None) -> str:
    """
    customized_redirect_map
    {
        ALIAS_0:
        {
            REDIRECT_PATH_0: redirect_path_0,
            REDIRECT_PATH_1: redirect_path_1,
        },
        ALIAS_1:
        {
            REDIRECT_PATH_0: redirect_path_0,
            REDIRECT_PATH_2: redirect_path_2,
        }
    }
    """

    path = path_builder(url, redirect_path)
    if customized_redirect_map is None:
        return path
    if alias in customized_redirect_map.keys():
        if redirect_path in customized_redirect_map[alias].keys():
            path = path_builder(url, customized_redirect_map[alias][redirect_path])
    return path
