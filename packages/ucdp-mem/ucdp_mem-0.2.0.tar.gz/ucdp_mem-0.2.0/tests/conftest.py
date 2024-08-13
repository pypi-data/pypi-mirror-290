"""Pytest Configuration and Fixtures."""

import os
from pathlib import Path
from unittest import mock

import ucdp as u
from pytest import fixture


@fixture
def prjroot(tmp_path):
    """Emulate prjroot."""
    with mock.patch.dict(os.environ, {"PRJROOT": str(tmp_path)}):
        yield tmp_path


@fixture
def techconfig():
    """Emulate prjroot."""
    paths = [Path(__file__).parent / "testdata"]
    with u.extend_sys_path(paths):
        yield
