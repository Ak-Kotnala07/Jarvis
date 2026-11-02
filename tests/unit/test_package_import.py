"""Verify the skeleton package can be imported."""


def test_package_imports() -> None:
    """The package root remains importable."""
    import jarvis

    assert jarvis is not None

