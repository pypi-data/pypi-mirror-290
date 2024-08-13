from pathlib import Path
from subprocess import (
    PIPE,
    Popen,
    run,
)
from typing import (
    Optional,
    Tuple,
)
from urllib.parse import urlparse

from quick_api_tests.logger.log import LOGGER


def create_and_write_file(file_path: Path, text=None):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if text:
        file_path.write_text(text)


def is_url(path):
    parsed = urlparse(path)
    return bool(parsed.scheme) and bool(parsed.netloc)


def run_command(command: str) -> Tuple[int, Optional[str]]:
    result = run(command, shell=True, stderr=PIPE, text=True)  # noqa: S602
    stderr = result.stderr
    return result.returncode, stderr


def format_file() -> None:
    # LOGGER.info(f"Linting generated code at: {path}")
    command_format = [
        'ruff',
        'format',
        './clients/http',
        './clients/grpc/stubs',
        './logic',
        './tests',
    ]
    run_command(' '.join(command_format))
    command_check = [
        'ruff',
        'check',
        './clients/http',
        './clients/grpc/stubs',
        './logic',
        './tests',
        '--fix',
    ]
    run_command(' '.join(command_check))
