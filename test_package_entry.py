import subprocess
import sys


def test_package_module_entry_shows_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "dataqa_cli", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "usage:" in result.stdout
    assert "--config" in result.stdout
