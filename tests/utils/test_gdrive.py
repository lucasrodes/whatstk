import os
import json

import pytest
from pydrive2.files import ApiRequestError

from whatstk.utils.gdrive import gdrive_init, _check_gdrive_config, _load_str_from_file_id
import whatstk


def test_init_1(tmpdir, mocker):
    # Create tmp secrets
    client_secret = {"field": 1}
    client_secret_file = tmpdir.join("client_secrets.json")
    with open(client_secret_file, 'w') as f:
        json.dump(client_secret, f)
    # Mock 1
    CONFIG_PATH = tmpdir.mkdir(".config")
    mocker.patch.object(whatstk.utils.gdrive, "CONFIG_PATH", CONFIG_PATH)
    mocker.patch.object(whatstk.utils.gdrive, "CLIENT_SECRETS_PATH", os.path.join(CONFIG_PATH, "client_secrets.json"))
    mocker.patch.object(whatstk.utils.gdrive, "SETTINGS_PATH", os.path.join(CONFIG_PATH, "settings.yaml"))
    mocker.patch.object(whatstk.utils.gdrive, "CREDENTIALS_PATH", os.path.join(CONFIG_PATH, "credentials.json"))
    mocker.patch("pydrive2.auth.GoogleAuth.CommandLineAuth", return_value=True)
    gdrive_init(client_secret_file)


def test_init_2(tmpdir, mocker):
    # Create tmp secrets
    client_secret = {"field": 1}
    client_secret_file = tmpdir.join("client_secrets.json")
    with open(client_secret_file, 'w') as f:
        json.dump(client_secret, f)
    # Mock 2
    CONFIG_PATH = tmpdir.join(".config2")
    mocker.patch.object(whatstk.utils.gdrive, "CONFIG_PATH", CONFIG_PATH)
    mocker.patch.object(whatstk.utils.gdrive, "CLIENT_SECRETS_PATH", os.path.join(CONFIG_PATH, "client_secrets.json"))
    mocker.patch.object(whatstk.utils.gdrive, "SETTINGS_PATH", os.path.join(CONFIG_PATH, "settings.yaml"))
    mocker.patch.object(whatstk.utils.gdrive, "CREDENTIALS_PATH", os.path.join(CONFIG_PATH, "credentials.json"))
    mocker.patch("pydrive2.auth.GoogleAuth.CommandLineAuth", return_value=True)
    gdrive_init(client_secret_file)


def test_check(tmpdir, mocker):
    with pytest.raises(ValueError):
        mocker.patch("os.path.isdir", return_value=False)
        _check_gdrive_config()
    with pytest.raises(ValueError):
        mocker.patch("os.path.isdir", return_value=True)
        mocker.patch("os.path.isfile", return_value=False)
        _check_gdrive_config()
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.path.isfile", return_value=True)
    _check_gdrive_config()


def test_load_2(mocker):
    mocker.patch("whatstk.utils.gdrive._check_gdrive_config", return_value=True)
    mocker.patch("pydrive2.auth.GoogleAuth", return_value=True)
    mocker.patch("pydrive2.drive.GoogleDrive", return_value=True)
    mocker.patch("pydrive2.drive.GoogleDrive.CreateFile", return_value=True)
    mocker.patch("pydrive2.files.GoogleDriveFile.FetchMetadata", return_value=True)
    mocker.patch("pydrive2.files.GoogleDriveFile.GetContentString", return_value="mock text")
    text = _load_str_from_file_id("some-id")
    assert isinstance(text, str)
