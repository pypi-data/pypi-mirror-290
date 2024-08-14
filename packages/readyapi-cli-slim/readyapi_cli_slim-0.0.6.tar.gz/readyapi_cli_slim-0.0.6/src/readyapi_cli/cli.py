from logging import getLogger
from pathlib import Path
from typing import Any, Union

import cligenius
from rich import print
from rich.padding import Padding
from rich.panel import Panel
from typing_extensions import Annotated

from readyapi_cli.discover import get_import_string
from readyapi_cli.exceptions import ReadyAPICLIException

from . import __version__
from .logging import setup_logging

app = cligenius.Cligenius(rich_markup_mode="rich")

setup_logging()
logger = getLogger(__name__)

try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]


def version_callback(value: bool) -> None:
    if value:
        print(f"ReadyAPI CLI version: [green]{__version__}[/green]")
        raise cligenius.Exit()


@app.callback()
def callback(
    version: Annotated[
        Union[bool, None],
        cligenius.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
) -> None:
    """
    ReadyAPI CLI - The [bold]readyapi[/bold] command line app. 😎

    Manage your [bold]ReadyAPI[/bold] projects, run your ReadyAPI apps, and more.

    Read more in the docs: [link]https://readyapi.khulnasoft.com/readyapi-cli/[/link].
    """


def _run(
    path: Union[Path, None] = None,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    workers: Union[int, None] = None,
    root_path: str = "",
    command: str,
    app: Union[str, None] = None,
    proxy_headers: bool = False,
) -> None:
    try:
        use_uvicorn_app = get_import_string(path=path, app_name=app)
    except ReadyAPICLIException as e:
        logger.error(str(e))
        raise cligenius.Exit(code=1) from None
    serving_str = f"[dim]Serving at:[/dim] [link]http://{host}:{port}[/link]\n\n[dim]API docs:[/dim] [link]http://{host}:{port}/docs[/link]"

    if command == "dev":
        panel = Panel(
            f"{serving_str}\n\n[dim]Running in development mode, for production use:[/dim] \n\n[b]readyapi run[/b]",
            title="ReadyAPI CLI - Development mode",
            expand=False,
            padding=(1, 2),
            style="black on yellow",
        )
    else:
        panel = Panel(
            f"{serving_str}\n\n[dim]Running in production mode, for development use:[/dim] \n\n[b]readyapi dev[/b]",
            title="ReadyAPI CLI - Production mode",
            expand=False,
            padding=(1, 2),
            style="green",
        )
    print(Padding(panel, 1))
    if not uvicorn:
        raise ReadyAPICLIException(
            "Could not import Uvicorn, try running 'pip install uvicorn'"
        ) from None
    uvicorn.run(
        app=use_uvicorn_app,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        root_path=root_path,
        proxy_headers=proxy_headers,
    )


@app.command()
def dev(
    path: Annotated[
        Union[Path, None],
        cligenius.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]ReadyAPI[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    host: Annotated[
        str,
        cligenius.Option(
            help="The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue]."
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        cligenius.Option(
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app."
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        cligenius.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = True,
    root_path: Annotated[
        str,
        cligenius.Option(
            help="The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar."
        ),
    ] = "",
    app: Annotated[
        Union[str, None],
        cligenius.Option(
            help="The name of the variable that contains the [bold]ReadyAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        cligenius.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
) -> Any:
    """
    Run a [bold]ReadyAPI[/bold] app in [yellow]development[/yellow] mode. 🧪

    This is equivalent to [bold]readyapi run[/bold] but with [bold]reload[/bold] enabled and listening on the [blue]127.0.0.1[/blue] address.

    It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

    If no path is passed, it tries with:

    - [blue]main.py[/blue]
    - [blue]app.py[/blue]
    - [blue]api.py[/blue]
    - [blue]app/main.py[/blue]
    - [blue]app/app.py[/blue]
    - [blue]app/api.py[/blue]

    It also detects the directory that needs to be added to the [bold]PYTHONPATH[/bold] to make the app importable and adds it.

    It detects the [bold]ReadyAPI[/bold] app object to use. By default it looks in the module or package for an object named:

    - [blue]app[/blue]
    - [blue]api[/blue]

    Otherwise, it uses the first [bold]ReadyAPI[/bold] app found in the imported module or package.
    """
    _run(
        path=path,
        host=host,
        port=port,
        reload=reload,
        root_path=root_path,
        app=app,
        command="dev",
        proxy_headers=proxy_headers,
    )


@app.command()
def run(
    path: Annotated[
        Union[Path, None],
        cligenius.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]ReadyAPI[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    host: Annotated[
        str,
        cligenius.Option(
            help="The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue]."
        ),
    ] = "0.0.0.0",
    port: Annotated[
        int,
        cligenius.Option(
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app."
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        cligenius.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = False,
    workers: Annotated[
        Union[int, None],
        cligenius.Option(
            help="Use multiple worker processes. Mutually exclusive with the --reload flag."
        ),
    ] = None,
    root_path: Annotated[
        str,
        cligenius.Option(
            help="The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar."
        ),
    ] = "",
    app: Annotated[
        Union[str, None],
        cligenius.Option(
            help="The name of the variable that contains the [bold]ReadyAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        cligenius.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
) -> Any:
    """
    Run a [bold]ReadyAPI[/bold] app in [green]production[/green] mode. 🚀

    This is equivalent to [bold]readyapi dev[/bold] but with [bold]reload[/bold] disabled and listening on the [blue]0.0.0.0[/blue] address.

    It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

    If no path is passed, it tries with:

    - [blue]main.py[/blue]
    - [blue]app.py[/blue]
    - [blue]api.py[/blue]
    - [blue]app/main.py[/blue]
    - [blue]app/app.py[/blue]
    - [blue]app/api.py[/blue]

    It also detects the directory that needs to be added to the [bold]PYTHONPATH[/bold] to make the app importable and adds it.

    It detects the [bold]ReadyAPI[/bold] app object to use. By default it looks in the module or package for an object named:

    - [blue]app[/blue]
    - [blue]api[/blue]

    Otherwise, it uses the first [bold]ReadyAPI[/bold] app found in the imported module or package.
    """
    _run(
        path=path,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        root_path=root_path,
        app=app,
        command="run",
        proxy_headers=proxy_headers,
    )


def main() -> None:
    app()
