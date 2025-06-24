import platform
from pathlib import Path

import typer

from weavster import cli_utils
from weavster.utils import to_snake_case

__version__ = "0.0.1"

app = typer.Typer(no_args_is_help=True)


@app.command()
def build() -> None:
    """
    Build the Weavster project
    """
    typer.echo("Building Weavster project...")
    # Placeholder for build logic


@app.command()
def init(
    directory: Path = typer.Argument(".", exists=True, file_okay=False, dir_okay=True),  # noqa: B008
    project_name: str = typer.Option(None, help="Project name (defaults to directory name)"),
) -> None:
    """
    Initialize a Weavster project
    """
    project_path = directory.resolve()
    name = project_name or project_path.name

    if any(project_path.iterdir()):
        typer.echo(f"❌ Directory '{project_path}' is not empty.")
        typer.echo("Please choose an empty directory or remove existing files.")
        raise typer.Exit(code=1)

    if project_name:
        # Create a new subdirectory using the project name
        name = to_snake_case(project_name)
        project_path = (directory / name).resolve()
        try:
            project_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            typer.echo(f"❌ Directory '{project_path}' already exists.")
            typer.echo("Please choose a different project name or remove the existing directory.")
            raise typer.Exit(code=1) from FileExistsError

    # Create the project structure
    # Create base directories
    (project_path / "connectors").mkdir(parents=True)
    (project_path / "routes").mkdir()
    (project_path / "filters").mkdir()
    (project_path / "transformers").mkdir()
    (project_path / "lookup_tables").mkdir()
    (project_path / "macros").mkdir()
    (project_path / "compiled/transformers").mkdir(parents=True)
    (project_path / "logs").mkdir()

    # Create stub files
    cli_utils.create_file(project_path / "weavster.yml", cli_utils.TEMPLATE_PROJECT_YML % name)
    cli_utils.create_file(project_path / "routes/lab_results_route.yml", cli_utils.TEMPLATE_ROUTE)
    cli_utils.create_file(project_path / "filters/.gitkeep", "")
    cli_utils.create_file(project_path / "transformers/normalize_lab_data.yml", cli_utils.TEMPLATE_TRANSFORMER)
    cli_utils.create_file(project_path / "macros/normalize_name.macro.yml", cli_utils.TEMPLATE_MACRO)
    cli_utils.create_file(project_path / "connectors/emr_connection.yml", cli_utils.TEMPLATE_CONNECTOR)

    cli_utils.create_file(project_path / ".gitignore", "compiled/\nlogs/\n")

    typer.secho(f"\n✅ Initialized Weavster project: {name}", fg=typer.colors.GREEN)
    typer.echo("Next steps:\n- Edit your config files\n- Run `weavster build`\n")


@app.command()
def version() -> None:
    """
    Get the current Weavster version
    """
    python_version = platform.python_version()
    os_name = platform.system().lower()
    arch = platform.machine().lower()

    typer.echo(f"Version:             {__version__}")
    typer.echo(f"Python version:      {python_version}")
    typer.echo(f"OS/Arch:             {os_name}/{arch}")


if __name__ == "__main__":
    app()
