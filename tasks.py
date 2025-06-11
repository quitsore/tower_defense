from invoke import task
import os
import sys

VENV_DIR = ".venv"
PYTHON = os.path.join(VENV_DIR, "bin", "python") if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "python.exe")

@task
def venv(c):
    """
    Create a virtualenv and install development deps.
    """
    c.run(f"{sys.executable} -m venv {VENV_DIR}")
    c.run(f"{PYTHON} -m pip install --upgrade pip")
    c.run(f"{PYTHON} -m pip install -e .[dev]")

@task
def install(c):
    """
    Install the package in editable mode.
    """
    c.run(f"{PYTHON} -m pip install -e .")

@task
def install_dev(c):
    """
    Install (or upgrade) the package in editable mode, syncing all deps.
    """
    c.run(f"{PYTHON} -m pip install --upgrade -e .[dev]")

@task
def clean(c):
    """
    Remove build artifacts.
    """
    c.run("rm -rf build/ dist/ *.egg-info")

@task(pre=[clean])
def build(c):
    """
    Build sdist and wheel.
    """
    c.run(f"{PYTHON} -m build")

@task
def upload(c, repository="pypi"):
    """
    Upload to PyPI or TestPyPI.
    """
    repo_arg = "--repository testpypi" if repository != "pypi" else ""
    c.run(f"{PYTHON} -m twine upload {repo_arg} dist/*")

@task
def test(c):
    """
    Run the test suite.
    """
    c.run(f"{PYTHON} -m pytest")

@task
def winexe(c):
    """
    Bundle a Windows executable via PyInstaller.
    """
    c.run(f"{PYTHON} -m pyinstaller --onefile --name tower_defense "
          f"--icon installer/icon.ico "
          f"--paths src "
          f"--add-data \"src/tower defense/resources;resources\" "
          f"--noconsole run.py")

import tomllib

def _get_version():
    # tomllib.load() wants a binary file
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]

@task(pre=[build, upload])
def publish(c):
    """
    Build, upload, tag, and push a new release.
    """
    version = _get_version()
    c.run(f"git tag v{version}")
    c.run("git push --tags")

