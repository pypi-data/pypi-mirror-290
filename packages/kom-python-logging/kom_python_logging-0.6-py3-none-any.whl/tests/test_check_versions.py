# tests/test_check_versions.py
import pytest
import subprocess
import sys
import os
import re
from workflow_scripts.check_versions import (
    get_current_version,
    get_latest_pypi_version,
    compare_versions,
    main,
)


def test_get_current_version(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data='version="0.5"'))
    version = get_current_version()
    assert version == "0.5"


def test_get_current_version_no_version(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    with pytest.raises(
        RuntimeError, match="Cannot find the version information in setup.py"
    ):
        get_current_version()


def test_get_latest_pypi_version(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "0.4"}}
    mocker.patch("requests.get", return_value=mock_response)

    package_name = "kom-python-logging"
    latest_version = get_latest_pypi_version(package_name)
    assert latest_version == "0.4"


def test_get_latest_pypi_version_error(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    package_name = "kom-python-logging"
    with pytest.raises(
        RuntimeError, match="Error fetching package information from PyPI: 404"
    ):
        get_latest_pypi_version(package_name)


def test_compare_versions_greater():
    current_version = "0.5"
    latest_version = "0.4"
    try:
        compare_versions(current_version, latest_version)
    except ValueError:
        pytest.fail("compare_versions() raised ValueError unexpectedly!")


def test_compare_versions_not_greater():
    current_version = "0.4"
    latest_version = "0.5"
    with pytest.raises(ValueError):
        compare_versions(current_version, latest_version)


def test_compare_versions_equal():
    current_version = "0.4"
    latest_version = "0.4"
    with pytest.raises(ValueError):
        compare_versions(current_version, latest_version)


def test_main(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data='version="0.5"'))
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "0.4"}}
    mocker.patch("requests.get", return_value=mock_response)
    mocker.patch("os.getenv", return_value="kom-python-logging")

    mock_print = mocker.patch("builtins.print")

    main()
    mock_print.assert_called_with(
        "Current version 0.5 is greater than the latest PyPI version 0.4"
    )


def test_main_script(mocker):
    # Read the version from setup.py
    with open("setup.py", "r") as file:
        setup_content = file.read()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', setup_content)
    if not match:
        pytest.fail("No version found in setup.py")
    current_version = match.group(1)

    # Mock necessary functions and values
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "0.4"}}
    mocker.patch("requests.get", return_value=mock_response)
    mocker.patch("os.getenv", return_value="kom-python-logging")

    # Run the script
    result = subprocess.run(
        [sys.executable, os.path.join("workflow_scripts", "check_versions.py")],
        capture_output=True,
        text=True,
    )

    # Assert the expected output
    expected_output = (
        f"Current version {current_version} is greater than the latest PyPI version 0.4"
    )
    assert expected_output in result.stdout
