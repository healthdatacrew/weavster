from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_typer_echo():
    """Mock typer.echo to capture output."""
    with patch("typer.echo") as mock_echo:
        yield mock_echo


@pytest.fixture
def mock_typer_secho():
    """Mock typer.secho to capture output."""
    with patch("typer.secho") as mock_secho:
        yield mock_secho


@pytest.fixture
def mock_create_file():
    """Mock cli_utils.create_file."""
    # We mock this function because it performs file system operations
    # and we want to assert that it was called with correct arguments.
    with patch("weavster.cli_utils.create_file") as mock_cf:
        yield mock_cf


@pytest.fixture
def mock_path_object():
    """
    A pytest fixture to provide a mock Path object for testing.
    """
    with patch("pathlib.Path") as mock_path:
        # Configure the mock Path object
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        yield mock_path_instance
