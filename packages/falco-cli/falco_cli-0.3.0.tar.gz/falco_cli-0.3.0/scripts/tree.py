# copied from https://github.com/Textualize/rich/blob/master/examples/tree.py
import os
import pathlib
import sys

from rich import print
from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.terminal_theme import DIMMED_MONOKAI
from rich.terminal_theme import SVG_EXPORT_THEME
from rich.text import Text
from rich.tree import Tree
# from rich.filesize import decimal


def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        # if path.name.startswith("."):
        #     continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: {escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            # file_size = path.stat().st_size
            # text_filename.append(f" ({decimal(file_size)})", "blue")
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(
        ":open_file_folder: project_name"
        # f":open_file_folder: [link file://{directory}]{directory}",
        # guide_style="bold bright_blue",
    )
    walk_directory(pathlib.Path(directory), tree)

    table = Table(title="Star Wars Movies")
    console = Console(record=True)
    with console.capture() as capture:
        console.print(tree)
    console.save_svg("docs/images/project-tree.svg", title="project blueprint tree", theme=DIMMED_MONOKAI)
