from unittest.mock import patch

from weavster.cli_utils import create_file


def test_create_file_creates_parent_directory_if_not_exists(mock_path_object):
    """
    Test that create_file calls mkdir with the correct arguments
    to create parent directories if they don't exist.
    """
    mock_path_object.parent.mkdir.assert_not_called()  # Ensure it's not called initially
    create_file(mock_path_object, "some content")
    mock_path_object.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)


def test_create_file_writes_content_to_file(mock_path_object):
    """
    Test that create_file calls write_text with the provided content.
    """
    content = "Hello, world!"
    create_file(mock_path_object, content)
    mock_path_object.write_text.assert_called_once_with(content)


def test_create_file_echos_creation_message(mock_path_object):
    """
    Test that create_file prints the correct creation message using typer.echo.
    We'll mock typer.echo to capture its output.
    """
    # Mock typer.echo to prevent actual console output during the test
    with patch("typer.echo") as mock_echo:
        create_file(mock_path_object, "test content")
        mock_echo.assert_called_once_with(f"Created: {mock_path_object}")


def test_create_file_with_different_path_and_content(mock_path_object):
    """
    Test with different path and content values to ensure flexibility.
    """
    mock_path_object.name = "another_file.txt"  # Give the mock a name for the f-string
    content = "Different content for a different file."
    with patch("typer.echo") as mock_echo:
        create_file(mock_path_object, content)
        mock_path_object.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_path_object.write_text.assert_called_once_with(content)
        mock_echo.assert_called_once_with(f"Created: {mock_path_object}")
