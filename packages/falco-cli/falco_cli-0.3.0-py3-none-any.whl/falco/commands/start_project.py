from __future__ import annotations

import shutil
import subprocess
from contextlib import suppress
from pathlib import Path
from typing import Annotated

import cappa
import httpx
from django.core.management import CommandError
from django.core.management.commands.startproject import Command as DjangoStartProject
from falco import falco_version
from falco.commands.htmx import Htmx
from falco.utils import clean_project_name
from falco.utils import get_falco_blueprints_path
from falco.utils import network_request_with_progress
from falco.utils import RICH_INFO_MARKER
from falco.utils import RICH_SUCCESS_MARKER
from falco.utils import simple_progress
from rich import print as rich_print
from rich.prompt import Prompt


class StartProjectPlus(DjangoStartProject):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--author-name", dest="author_name")
        parser.add_argument("--author-email", dest="author_email")


def get_authors_info() -> tuple[str, str]:
    default_author_name = "Tobi DEGNON"
    default_author_email = "tobidegnon@proton.me"
    git_config_cmd = ["git", "config", "--global", "--get"]
    try:
        user_name_cmd = subprocess.run([*git_config_cmd, "user.name"], capture_output=True, text=True, check=False)
        user_email_cmd = subprocess.run([*git_config_cmd, "user.email"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return default_author_name, default_author_email
    if user_email_cmd.returncode != 0:
        return default_author_name, default_author_email
    return (
        user_name_cmd.stdout.strip("\n"),
        user_email_cmd.stdout.strip("\n"),
    )


def is_new_falco_cli_available() -> bool:
    try:
        with network_request_with_progress(
            "https://pypi.org/pypi/falco-cli/json",
            "Checking for new falco version...",
        ) as response:
            latest_version = response.json()["info"]["version"]
            current_version = falco_version
            return latest_version != current_version
    except cappa.Exit:
        return False


@cappa.command(help="Initialize a new django project the falco way.")
class StartProject:
    project_name: Annotated[
        str,
        cappa.Arg(parse=clean_project_name, help="Name of the project to create."),
    ]
    directory: Annotated[Path | None, cappa.Arg(help="Directory to create project in.")]
    skip_new_version_check: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--skip-new-version-check",
            help="Do not check for new version.",
        ),
    ]

    def __call__(self) -> None:
        if not self.skip_new_version_check and is_new_falco_cli_available():
            message = (
                f"{RICH_INFO_MARKER} A new version of falco-cli is available. To upgrade, run "
                f"[green]pip install -U falco-cli."
            )
            rich_print(message)

            response = Prompt.ask(
                f"{RICH_INFO_MARKER}Do you want to stop to upgrade your current falco-cli version? (Y/n)",
                default="Y",
            )

            if response.lower() == "y":
                rich_print(
                    f"{RICH_INFO_MARKER}To see the latest features and improvements, visit https://github.com/Tobi-De/falco/releases."
                )
                raise cappa.Exit(code=0)

        project_dir = self.init_project()
        msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
        msg += (
            f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
            f"https://github.com/Tobi-De/falco"
        )

        rich_print(msg)
        self.update_htmx(project_dir)

    def init_project(self) -> Path:
        project_template_path = get_falco_blueprints_path() / "project_name"
        author_name, author_email = get_authors_info()
        with simple_progress("Initializing your new django project... :sunglasses:"):
            argv = [
                "falco",
                "startproject",
                self.project_name,
                "--template",
                str(project_template_path),
                "-e=py,html,toml,md,json,js,sh,yml,ipynb",
                f"--author-name={author_name}",
                f"--author-email={author_email}",
                "--traceback",
            ]
            if self.directory:
                argv.insert(3, str(self.directory.resolve()))
            try:
                StartProjectPlus().run_from_argv(argv)
            except CommandError as e:
                raise cappa.Exit(str(e), code=1) from e

            project_dir = self.directory or Path(self.project_name)

            shutil.copytree(project_template_path / ".github", project_dir / ".github")
        return project_dir

    def update_htmx(self, project_dir: Path):
        with suppress(cappa.Exit, httpx.TimeoutException, httpx.ConnectError):
            Htmx(
                version="latest",
                output=project_dir / self.project_name / "static" / "vendors" / "htmx" / "htmx.min.js",
            )()
