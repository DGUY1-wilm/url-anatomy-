import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from url_anatomy import analyze, SIMPLE_EXAMPLE, COMPLEX_EXAMPLE


def as_dict(url):
    return {part.strip(): value for part, value, _ in analyze(url)}


def test_simple():
    d = as_dict(SIMPLE_EXAMPLE)
    assert d["scheme"] == "https"
    assert d["host"] == "www.example.com"
    assert d["subdomain"] == "www"
    assert d["path"] == "/blog/hello-world"
    assert d["port"] == "(implied 443)"


def test_complex():
    d = as_dict(COMPLEX_EXAMPLE)
    assert d["username"] == "user"
    assert d["port"] == "8443"
    assert d["q"] == "red shoes"
    assert d["fragment"] == "reviews"
    assert d["segment 3"] == "running shoes"
    assert d["file 4"] == "index.html"
    assert d["suffix"] == "co.uk"
    assert d["domain"] == "example"
    assert d["subdomain"] == "shop.eu"
