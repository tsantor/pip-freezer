import tempfile
from pathlib import Path

import pytest
from pipfreezer import PackageData
from pipfreezer import find_requirements_files
from pipfreezer import get_package_data_from_json_output
from pipfreezer import get_package_data_from_requirements
from pipfreezer import get_pip_dict
from pipfreezer import get_pip_list_as_json
from pipfreezer import get_pip_list_outdated_as_json
from pipfreezer import open_requirements
from pipfreezer import save_requirements
from pipfreezer import update_requirements_file

# from pipfreezer import run


@pytest.fixture()
def requirements_lines():
    return ["# Comment\n", "requests==2.25.1\n", "flask==1.1.2\n"]


@pytest.fixture()
def requirements_file(requirements_lines):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("".join(requirements_lines))
    return tmp


@pytest.fixture()
def pip_list_as_json(mocker):
    """
    Mock the return value of the subprocess.run function:
    pip list --format json
    """
    mock_result = mocker.Mock()
    mock_result.stdout = '[{"name": "requests", "version": "2.25.1"}, {"name": "flask", "version": "1.1.2"}]'
    mocker.patch("subprocess.run", return_value=mock_result)

    return get_pip_list_as_json()


@pytest.fixture()
def pip_list_outdated_as_json(mocker):
    """
    Mock the return value of the subprocess.run function:
    pip list --outdated --format json
    """
    mock_result = mocker.Mock()
    mock_result.stdout = '[{"name": "requests", "version": "2.26.0"}, {"name": "flask", "version": "1.2.0"}]'
    mocker.patch("subprocess.run", return_value=mock_result)

    return get_pip_list_outdated_as_json()


def test_get_package_data_from_json_output(pip_list_as_json):
    assert get_package_data_from_json_output(pip_list_as_json) == [
        PackageData("requests==2.25.1"),
        PackageData("flask==1.1.2"),
    ]


def test_get_pip_dict(pip_list_as_json):
    assert get_pip_dict(pip_list_as_json) == {"requests": "2.25.1", "flask": "1.1.2"}


def test_get_pip_dict_outdated(pip_list_outdated_as_json):
    assert get_pip_dict(pip_list_outdated_as_json) == {
        "requests": "2.26.0",
        "flask": "1.2.0",
    }


def test_open_and_save_requirements(requirements_file, requirements_lines):
    # Test open_requirements
    lines = open_requirements(requirements_file.name)
    assert lines == requirements_lines

    # Test save_requirements
    new_lines = ["requests==2.25.1\n", "flask==2.0.1\n"]
    save_requirements(requirements_file.name, new_lines)
    lines = open_requirements(requirements_file.name)
    assert lines == new_lines

    # Clean up the temporary file
    Path(requirements_file.name).unlink()


def test_find_requirements_files(mocker):
    # Mock the return value of Path().rglob
    mock_files = [Path("requirements.txt"), Path("requirements-dev.txt")]
    mocker.patch.object(Path, "rglob", return_value=mock_files)

    # Call the function and check the result
    files = find_requirements_files()
    assert files == mock_files


def test_get_package_data_from_requirements(mocker, requirements_file):
    # Mock the return value of Path().rglob
    mock_files = [Path(requirements_file.name)]
    mocker.patch.object(Path, "rglob", return_value=mock_files)

    packages = get_package_data_from_requirements()
    assert packages == [PackageData("requests==2.25.1"), PackageData("flask==1.1.2")]

    # Clean up the temporary file
    Path(requirements_file.name).unlink()


def test_update_requirements_file(requirements_file):
    # Define the package_dict
    package_dict = {"requests": "2.25.1", "flask": "2.0.1"}

    # Call the function and check the result
    updated, not_installed = update_requirements_file(
        requirements_file.name, package_dict
    )
    assert updated == ["flask 1.1.2 => 2.0.1"]
    assert not_installed == []

    # Check the content of the file
    lines = open_requirements(requirements_file.name)
    assert lines == ["# Comment\n", "requests==2.25.1\n", "flask==2.0.1\n"]

    # Clean up the temporary file
    Path(requirements_file.name).unlink()
