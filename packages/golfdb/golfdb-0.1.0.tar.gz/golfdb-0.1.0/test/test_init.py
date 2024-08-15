"""Tests for the top-level golfdb package."""

import golfdb

import test


def test_version_defined() -> None:
    """Basic sanity check that golfdb.__version__ is defined."""
    assert hasattr(golfdb, "__version__")


def test_test_import() -> None:
    """
    Basic sanity check that test utilities/helpers can be imported.

    This makes sure that we can import the testing utility package in
    ``./__init__.py`` in all environments we test in. The test will always pass
    if the import succeeds; any failures would happen on the ``import test``
    line above.

    Note that this test doesn't really belong in this file - which should be
    focused on testing :mod:`golfdb` - but until we actually have tests (and
    test utilities), I'm not going to figure out where "tests for testing the
    test utilities" should live. (Or if it will even exist.)
    """
    assert hasattr(test, "__doc__")
