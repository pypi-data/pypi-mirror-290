from pathlib import Path

import pytest
from cligenius.testing import CliRunner
from readyapi_cli.discover import get_import_string
from readyapi_cli.exceptions import ReadyAPICLIException

from .utils import changing_dir

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_no_uvicorn() -> None:
    import readyapi_cli.cli
    import uvicorn

    readyapi_cli.cli.uvicorn = None  # type: ignore[attr-defined, assignment]

    with changing_dir(assets_path):
        result = runner.invoke(readyapi_cli.cli.app, ["dev", "single_file_app.py"])
        assert result.exit_code == 1
        assert result.exception is not None
        assert (
            "Could not import Uvicorn, try running 'pip install uvicorn'"
            in result.exception.args[0]
        )

    readyapi_cli.cli.uvicorn = uvicorn  # type: ignore[attr-defined]


def test_no_readyapi() -> None:
    import readyapi_cli.discover
    from readyapi import ReadyAPI

    readyapi_cli.discover.ReadyAPI = None  # type: ignore[attr-defined, assignment]
    with changing_dir(assets_path):
        with pytest.raises(ReadyAPICLIException) as exc_info:
            get_import_string(path=Path("single_file_app.py"))
        assert "Could not import ReadyAPI, try running 'pip install readyapi'" in str(
            exc_info.value
        )

    readyapi_cli.discover.ReadyAPI = ReadyAPI  # type: ignore[attr-defined]
