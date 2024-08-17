from __future__ import annotations

from pathlib import Path
import shutil
from typing import List

import nox

supported_python_versions = ["3.10", "3.11", "3.12"]

default_python = sorted(supported_python_versions)[-2]

repo_root = Path(__file__).parent


@nox.session(reuse_venv=True)
def build(session):
    session.install("build", "twine")
    session.run("python", "-m", "build")
    session.run("python", "-m", "twine", "check", "--strict", "dist/*")


@nox.session(reuse_venv=True)
def requirements(session):
    shutil.copyfile(
        repo_root / "requirements.in", repo_root / "requirements.txt"
    )


@nox.session(reuse_venv=True)
def format(session):
    session.install(
        "isort",
        "ruff"
    )
    session.run("isort", ".")
    session.run("ruff", "format", "src")


@nox.session(python=supported_python_versions)
def fulltest(session):
    session.notify(f"pytest-{session.python}")
    session.notify(f"doctest-{session.python}")
    session.notify(f"e2etest-{session.python}")
    session.notify(f"typing-{session.python}")


@nox.session(python=supported_python_versions)
def pytest(session):
    session.install(".[markdown]", "pytest", "coverage[toml]")
    session.run(*_coverage_cmd(session.name, ["pytest", "test"]))


@nox.session(python=supported_python_versions)
def doctest(session):
    session.install(".", "pytest", "coverage[toml]")
    session.run(
        *_coverage_cmd(session.name, ["pytest", "--doctest-modules", "src"])
    )


@nox.session(python=supported_python_versions)
def e2etest(session):
    session.install(".[docs]", "coverage[toml]")
    session.run(
        *_coverage_cmd(session.name, _sphinx_build_modulecmd(session_name=session.name))
    )


@nox.session(reuse_venv=True)
def lint(session):
    session.install(
        "ruff",
    )
    session.run("ruff", "check", "src", "--fix", "--unsafe-fixes")


@nox.session(reuse_venv=True)
def docstringstyle(session):
    session.install("pydocstyle", "toml")
    session.run("pydocstyle", "src")


@nox.session(reuse_venv=True, python=supported_python_versions)
def typing(session):
    session.install(
        ".[markdown]",
        "mypy",
        "lxml",
        "docutils-stubs",
        "importlib_metadata",
    )
    session.run("mypy", "--python-version", session.python, "src")


@nox.session(reuse_venv=True)
def coverage(session):
    session.install(".", "coverage[toml]")
    session.run("coverage", "combine", "--keep")
    session.run("coverage", "xml")
    session.run("coverage", "html")
    session.run("coverage", "report")


@nox.session(python=default_python, reuse_venv=True)
def docs(session):
    session.install(".[docs]")
    # session.run(*_python_cmd(_sphinx_apidoc_modulecmd()))
    session.run(*_python_cmd(_sphinx_build_modulecmd()))


def _sphinx_apidoc_modulecmd() -> List[str]:
    return [
        "sphinx.ext.apidoc",
        "-o",
        "docs/apidoc",
        "--force",
        "--no-toc",
        "--separate",
        "--module-first",
        "src",
    ]


def _sphinx_build_modulecmd(build_root: str = "build", session_name: str = "sphinx", builder: str = "html") -> List[str]:
    return [
        "sphinx",
        "-b",
        builder,
        "-d",
        f"{build_root}/{session_name}/doctrees",
        "-E",
        "-n",
        "-W",
        "--keep-going",
        "-T",
        "docs",
        f"{build_root}/{session_name}/{builder}",
    ]


def _python_cmd(modulecmd: List[str]) -> List[str]:
    return ["python", "-m", *modulecmd]


def _coverage_cmd(context: str, modulecmd: List[str]) -> List[str]:
    return [
        "python",
        "-m",
        "coverage",
        "run",
        f"--context={context}",
        "-m",
        *modulecmd,
    ]
