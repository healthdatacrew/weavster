from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

from weavster.cli import __version__, app

runner = CliRunner()


@pytest.fixture
def mock_cli_utils_templates():
    """Mock the TEMPLATE constants in cli_utils to ensure predictable content."""
    with (
        patch("weavster.cli_utils.TEMPLATE_PROJECT_YML", "mock_project_yml_content_%s"),
        patch("weavster.cli_utils.TEMPLATE_ROUTE", "mock_route_content"),
        patch("weavster.cli_utils.TEMPLATE_TRANSFORMER", "mock_transformer_content"),
        patch("weavster.cli_utils.TEMPLATE_MACRO", "mock_macro_content"),
        patch("weavster.cli_utils.TEMPLATE_CONNECTOR", "mock_connector_content"),
    ):
        yield


def test_build_command(mock_typer_echo):
    """
    Test the 'build' command prints the correct message.
    """
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 0
    mock_typer_echo.assert_called_once_with("Building Weavster project...")


# --- Tests for `version` command ---


def test_version_command(mock_typer_echo):
    """
    Test the 'version' command prints the correct version info.
    We mock `platform` functions to ensure consistent output.
    """
    with (
        patch("platform.python_version", return_value="3.9.10"),
        patch("platform.system", return_value="Linux"),
        patch("platform.machine", return_value="x86_64"),
    ):
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        expected_calls = [
            f"Version:             {__version__}",
            "Python version:      3.9.10",
            "OS/Arch:             linux/x86_64",
        ]
        # Verify that typer.echo was called with each expected line
        for call_arg in expected_calls:
            mock_typer_echo.assert_any_call(call_arg)
        # Verify the total number of calls to ensure no extra output
        assert mock_typer_echo.call_count == len(expected_calls)


# --- Tests for `init` command ---


def test_init_command_no_args(monkeypatch, mock_typer_secho, mock_create_file):
    """
    Test 'init' command with no arguments.
    Verifies creation of subdirectories and stub files.
    """
    mock_resolved_path = MagicMock(spec=Path)
    mock_resolved_path.name = "test_project"
    mock_resolved_path.__str__.return_value = "/home/mock_user/test_project"
    mock_resolved_path.iterdir.return_value = []

    mock_connectors_path = MagicMock(spec=Path)
    mock_routes_path = MagicMock(spec=Path)
    mock_filters_path = MagicMock(spec=Path)
    mock_transformers_path = MagicMock(spec=Path)
    mock_lookup_tables_path = MagicMock(spec=Path)
    mock_macros_path = MagicMock(spec=Path)
    mock_compiled_transformers_path = MagicMock(spec=Path)
    mock_logs_path = MagicMock(spec=Path)

    # NEW: Mock for the weavster.yml file path directly under project_path
    mock_weavster_yml_path = MagicMock(spec=Path)
    mock_weavster_yml_path.__str__.return_value = "/home/mock_user/test_project/weavster.yml"

    # NEW: Mocks for files within subdirectories
    mock_dummy_connector_file_path = MagicMock(spec=Path)
    mock_dummy_connector_file_path.__str__.return_value = "/home/mock_user/test_project/connectors/dummy_connector.py"

    mock_dummy_route_file_path = MagicMock(spec=Path)
    mock_dummy_route_file_path.__str__.return_value = "/home/mock_user/test_project/routes/dummy_route.py"

    mock_dummy_transformer_file_path = MagicMock(spec=Path)
    mock_dummy_transformer_file_path.__str__.return_value = (
        "/home/mock_user/test_project/transformers/dummy_transformer.py"
    )

    mock_dummy_macro_file_path = MagicMock(spec=Path)
    mock_dummy_macro_file_path.__str__.return_value = "/home/mock_user/test_project/macros/dummy_macro.py"
    mock_resolved_path_side_effects = [
        mock_connectors_path,
        mock_routes_path,
        mock_filters_path,
        mock_transformers_path,
        mock_lookup_tables_path,
        mock_macros_path,
        mock_compiled_transformers_path,
        mock_logs_path,
        mock_weavster_yml_path,
        mock_resolved_path,
        mock_resolved_path,
        mock_resolved_path,
        mock_resolved_path,
        mock_resolved_path,
        mock_resolved_path,
    ]

    mock_resolved_path.__truediv__.side_effect = mock_resolved_path_side_effects

    mock_connectors_path.__truediv__.return_value = mock_dummy_connector_file_path
    mock_routes_path.__truediv__.return_value = mock_dummy_route_file_path
    mock_transformers_path.__truediv__.return_value = mock_dummy_transformer_file_path
    mock_macros_path.__truediv__.return_value = mock_dummy_macro_file_path

    monkeypatch.setattr(Path, "resolve", lambda self: mock_resolved_path)
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0

    assert "✅ Initialized Weavster project: test_project" in mock_typer_secho.call_args[0][0]

    expected_trudiv_calls = [
        call("connectors"),
        call("routes"),
        call("filters"),
        call("transformers"),
        call("lookup_tables"),
        call("macros"),
        call("compiled/transformers"),
        call("logs"),
    ]
    mock_resolved_path.__truediv__.assert_has_calls(expected_trudiv_calls, any_order=False)
    assert mock_resolved_path.__truediv__.call_count == len(mock_resolved_path_side_effects)

    mock_connectors_path.mkdir.assert_called_once_with(parents=True)
    mock_routes_path.mkdir.assert_called_once_with()  # Default parents=False
    mock_filters_path.mkdir.assert_called_once_with()
    mock_transformers_path.mkdir.assert_called_once_with()
    mock_lookup_tables_path.mkdir.assert_called_once_with()
    mock_macros_path.mkdir.assert_called_once_with()
    mock_compiled_transformers_path.mkdir.assert_called_once_with(parents=True)
    mock_logs_path.mkdir.assert_called_once_with()

    assert mock_create_file.call_count == 7


# def test_init_command_in_empty_current_directory(mock_typer_echo, mock_typer_secho, mock_create_file):
#     """
#     Test 'init' command in an empty current directory using default project name.
#     Verifies creation of subdirectories and stub files.
#     """

#     result = runner.invoke(app, ["init"])

#     assert result.exit_code == 0
#     mock_typer_secho.assert_called_once()
#     assert "✅ Initialized Weavster project: my_current_project" in mock_typer_secho.call_args[0][0]

#     # When `project_name` is None, `project_path` is the existing directory (`.`).
#     # Its `mkdir` method should *not* be called.
#     # assert not root_path_mock._mock_mkdir_called

#     # Verify that all expected *subdirectories* within the project path were created
#     expected_relative_dirs = [
#         "connectors",
#         "routes",
#         "filters",
#         "transformers",
#         "lookup_tables",
#         "macros",
#         "compiled",
#         "compiled/transformers",
#         "logs",
#     ]
#     # for rel_path in expected_relative_dirs:
#     #     full_mock_path_str = f"./{rel_path}"
#     #     assert full_mock_path_str in mock_path_instances
#     #     dir_mock = mock_path_instances[full_mock_path_str]
#     #     assert dir_mock._mock_mkdir_called, f"Expected mkdir to be called on {full_mock_path_str}"

#     # # Verify `cli_utils.create_file` was called for all stub files
#     # assert mock_create_file.call_count == 7

#     # # Check specific file creation calls with their mocked path objects and content
#     # mock_create_file.assert_any_call(
#     #     mock_path_instances["./weavster.yml"],  # Path object for ./weavster.yml
#     #     f"mock_project_yml_content_my_current_project",  # Uses `name` (snake_cased project name)
#     # )
#     # mock_create_file.assert_any_call(mock_path_instances["./routes/lab_results_route.yml"], "mock_route_content")
#     # mock_create_file.assert_any_call(mock_path_instances["./filters/.gitkeep"], "")
#     # mock_create_file.assert_any_call(
#     #     mock_path_instances["./transformers/normalize_lab_data.yml"], "mock_transformer_content"
#     # )
#     # mock_create_file.assert_any_call(mock_path_instances["./macros/normalize_name.macro.yml"], "mock_macro_content")
#     # mock_create_file.assert_any_call(mock_path_instances["./connectors/emr_connection.yml"], "mock_connector_content")
#     # mock_create_file.assert_any_call(mock_path_instances["./.gitignore"], "compiled/\nlogs/\n")


def test_init_command_non_empty_current_directory(
    monkeypatch,
    mock_typer_echo,
):
    """
    Test 'init' command when the current directory is not empty.
    Should raise Typer.Exit(code=1) and print error messages.
    """

    mock_resolved_path = MagicMock(spec=Path)
    mock_resolved_path.name = "my_non_empty_project"
    mock_resolved_path.__str__.return_value = "/home/mock_user/my_non_empty_project"
    mock_resolved_path.iterdir.return_value = iter([MagicMock()])

    monkeypatch.setattr(Path, "resolve", lambda self: mock_resolved_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 1
    mock_typer_echo.assert_any_call(f"❌ Directory '{mock_resolved_path.__str__.return_value}' is not empty.")
    mock_typer_echo.assert_any_call("Please choose an empty directory or remove existing files.")
    assert mock_typer_echo.call_count == 2  # Ensure only these two calls were made


def test_init_command_new_project_name_in_empty_parent_dir(
    monkeypatch, mock_typer_echo, mock_typer_secho, mock_create_file
):
    """
    Test 'init' command with a new project name in an empty parent directory.
    Verifies that the new project directory and its subdirectories are created.
    """

    mock_resolved_path = MagicMock(spec=Path)
    mock_resolved_path.name = "test_project"
    mock_resolved_path.__str__.return_value = "/home/mock_user/test_project"
    mock_resolved_path.iterdir.return_value = []  # Ensure parent directory is empty

    project_name_input = "MyNewProject"
    snake_case_project_name = "my_new_project"  # Expected output from to_snake_case

    monkeypatch.setattr(Path, "resolve", lambda self: mock_resolved_path)

    result = runner.invoke(app, ["init", "--project-name", project_name_input])

    assert result.exit_code == 0
    mock_typer_secho.assert_called_once()
    # Verify the success message uses the *original* project name
    assert f"✅ Initialized Weavster project: {snake_case_project_name}" in mock_typer_secho.call_args[0][0]

    # Verify that the new project directory itself was created
    expected_project_path_str = f"./{snake_case_project_name}"
    assert expected_project_path_str in mock_path_instances
    new_project_dir_mock = mock_path_instances[expected_project_path_str]
    assert new_project_dir_mock._mock_mkdir_called, "Expected new project directory to be created"

    # Verify all subdirectories within the new project path were created
    expected_relative_dirs_within_project = [
        "connectors",
        "routes",
        "filters",
        "transformers",
        "lookup_tables",
        "macros",
        "compiled",
        "compiled/transformers",
        "logs",
    ]
    # for rel_path in expected_relative_dirs_within_project:
    #     full_mock_path_str = f"{expected_project_path_str}/{rel_path}"
    #     assert full_mock_path_str in mock_path_instances
    #     dir_mock = mock_path_instances[full_mock_path_str]
    #     assert dir_mock._mock_mkdir_called, f"Expected mkdir to be called on {full_mock_path_str}"
    #
    # # Verify `cli_utils.create_file` calls for files within the new project directory
    # assert mock_create_file.call_count == 7
    # mock_create_file.assert_any_call(
    #     mock_path_instances[f"{expected_project_path_str}/weavster.yml"],
    #     f"mock_project_yml_content_{snake_case_project_name}",  # Uses `name` (snake_cased) for template
    # )
    # mock_create_file.assert_any_call(
    #     mock_path_instances[f"{expected_project_path_str}/.gitignore"], "compiled/\nlogs/\n"
    # )


# def test_init_command_new_project_name_directory_already_exists(
#     mock_path_recursive,
#     mock_typer_echo,
# ):
#     """
#     Test 'init' command when the target new project directory already exists.
#     Should raise Typer.Exit(code=1) and print error messages.
#     """
#     root_path_mock = mock_path_recursive["root_path"]
#     mock_path_instances = mock_path_recursive["mock_path_instances"]
#
#     root_path_mock.iterdir.return_value = iter([])  # Ensure parent directory is empty
#
#     project_name_input = "Existing Project Dir"
#     snake_case_project_name = "existing_project_dir"
#
#     # Pre-simulate that the target directory already exists on disk
#     existing_project_dir_mock = root_path_mock / snake_case_project_name
#     existing_project_dir_mock._exists_on_disk = True  # Mark as existing
#     existing_project_dir_mock._is_dir = True  # Mark as a directory
#
#     with patch("weavster.utils.to_snake_case", return_value=snake_case_project_name):
#         result = runner.invoke(app, ["init", "--project-name", project_name_input])
#
#         assert result.exit_code == 1
#         mock_typer_echo.assert_any_call(f"❌ Directory '{existing_project_dir_mock._full_path}' already exists.")
#         mock_typer_echo.assert_any_call("Please choose a different project name or remove the existing directory.")
#         assert mock_typer_echo.call_count == 2  # Ensure only these two calls were made
#
#         # Verify that mkdir was attempted on the existing directory and it raised the error
#         assert existing_project_dir_mock._mock_mkdir_called, "Expected mkdir to be called on the existing directory"
