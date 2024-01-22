# tests/test_run.py

from topo_cicd_test.run import run


def test_run():
    assert run() == "Hello, World!"
