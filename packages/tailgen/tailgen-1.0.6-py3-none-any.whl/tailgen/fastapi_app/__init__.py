from pathlib import Path
import subprocess
from sys import platform
from time import sleep
import typer
import shutil
from tailgen import DELAY_DURATION
from tailgen.helpers import _get_setup_paths
from rich.progress import Progress

package_path = _get_setup_paths()


def _create_fastapi_project(project_dir: Path) -> None:
    """Create FastAPI Project"""
    sleep(DELAY_DURATION)

    venv_dir = project_dir / "venv"
    pip_executable = (
        "Scripts/pip.exe"
        if platform.startswith("win32") or platform.startswith("cygwin")
        else "bin/pip"
    )

    install_process = subprocess.Popen(
        [
            str(venv_dir / pip_executable),
            "install",
            "fastapi[standard]",
            "Jinja2",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    typer.secho("Installing dependencies...", fg=typer.colors.GREEN)

    while install_process.poll() is None:
        output = install_process.stdout.readline().strip()
        if output:
            typer.secho(output, fg=typer.colors.YELLOW)

    sleep(DELAY_DURATION)
    errors = install_process.stderr.read().strip()

    if errors:
        if "A new release of pip is available" in errors:
            typer.secho(
                "Notice: pip is outdated. Consider updating.", fg=typer.colors.RED
            )

        else:
            error_message = f"Error installing Flask: {errors}"
            raise RuntimeError(error_message)

    sleep(DELAY_DURATION)

    typer.secho(
        "Fastapi, Jinja2, and Uvicorn installed successfully.", fg=typer.colors.GREEN
    )

    sleep(DELAY_DURATION)

    typer.secho("Creating base FastAPI application...", fg=typer.colors.GREEN)

    source = Path(package_path.fastapi) / "main.txt"

    destination = Path(project_dir) / "main.py"

    try:
        shutil.copyfile(source, destination)

    except Exception as e:
        raise Exception(f"Failed to create base FastAPI file: {str(e)}")

    sleep(DELAY_DURATION)

    typer.secho("Creating static and templates directories.", fg=typer.colors.GREEN)
    # create static/ and templates/
    (project_dir / "static").mkdir(exist_ok=True)
    (project_dir / "templates").mkdir(exist_ok=True)

    typer.secho("Creating index HTML file", fg=typer.colors.GREEN)

    source = Path(package_path.fastapi) / "base.txt"
    destination = Path(project_dir) / "templates" / "base.html"

    try:
        shutil.copyfile(source, destination)

    except Exception as e:
        raise Exception(f"Failed to create base HTML file: {str(e)}")

    sleep(DELAY_DURATION)

    typer.secho("Completed FastAPI setup", fg=typer.colors.GREEN)


def _install_and_configure_tailwindcss_fastapi(project_dir: Path) -> None:
    """Install and configure Tailwind CSS"""

    with Progress() as progress:
        task = progress.add_task("[blue]Installing Tailwind CSS...", total=1)

        install_process = subprocess.Popen(
            [
                "npm",
                "install",
                "tailwindcss",
                "--prefix",
                project_dir.as_posix(),
                "--save-dev",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        for line in iter(install_process.stdout.readline, ""):
            progress.update(task, advance=1, color="red")

        # Wait for the installation process to complete
        install_process.communicate()

    typer.secho("Tailwind CSS installed successfully!", fg=typer.colors.GREEN)

    sleep(DELAY_DURATION)

    typer.secho("Creating Tailwind config file...", fg=typer.colors.GREEN)

    source = Path(package_path.fastapi) / "tailwind_config.txt"
    destination = project_dir / "tailwind.config.js"
    try:
        shutil.copyfile(source, destination)
    except Exception as e:
        raise Exception(f"Failed to create base HTML file: {str(e)}")

    sleep(DELAY_DURATION)

    typer.secho("Creating file for input CSS", fg=typer.colors.GREEN)

    static_dir = project_dir / "static"
    (static_dir / "src").mkdir(exist_ok=True)
    with open(static_dir / "src" / "input.css", "w") as f:
        f.write(
            """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        )

    sleep(DELAY_DURATION)

    typer.secho("Completed tailwind config", fg=typer.colors.GREEN)
