import json
import os
import stat

import pytest

from whatstk.utils.gdrive import gdrive_init, _check_gdrive_config, _load_str_from_file_id
import whatstk

# These tests exercise the Google Drive code path, not its deprecation, which has its own tests.
pytestmark = pytest.mark.filterwarnings("ignore:Google Drive support is deprecated:FutureWarning")


def test_init_1(tmpdir, mocker):
    # Create tmp secrets
    client_secret = {"field": 1}
    client_secret_file = tmpdir.join("client_secrets.json")
    with open(client_secret_file, "w") as f:
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
    with open(client_secret_file, "w") as f:
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


# --- Report #1611: credential files must not be readable by other local users -------------------


requires_posix = pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits are not honoured on Windows")


def _init_into(tmpdir, mocker, source_mode=0o600) -> dict:
    """Run gdrive_init against a throwaway config dir and return the paths it wrote."""
    client_secret_file = tmpdir.join("client_secrets.json")
    with open(client_secret_file, "w") as f:
        json.dump({"installed": {"client_secret": "SUPERSECRET"}}, f)
    if os.name != "nt":
        os.chmod(str(client_secret_file), source_mode)

    config_path = str(tmpdir.mkdir(".config-perms"))
    paths = {
        "CONFIG_PATH": config_path,
        "CLIENT_SECRETS_PATH": os.path.join(config_path, "client_secrets.json"),
        "SETTINGS_PATH": os.path.join(config_path, "settings.yaml"),
        "CREDENTIALS_PATH": os.path.join(config_path, "credentials.json"),
    }
    for name, value in paths.items():
        mocker.patch.object(whatstk.utils.gdrive, name, value)
    mocker.patch("pydrive2.auth.GoogleAuth.CommandLineAuth", return_value=True)

    gdrive_init(client_secret_file)
    return paths


def _mode(path) -> int:
    return stat.S_IMODE(os.stat(path).st_mode)


@requires_posix
def test_credentials_are_not_readable_by_other_users(tmpdir, mocker):
    """The client secret and settings must land at 0600 inside a 0700 directory.

    Report #1611: the directory was created with the umask (0755) and the files copied with
    shutil.copyfile (0644), leaving the OAuth client secret world-readable.
    """
    os.umask(0o022)  # the permissive default the report assumes
    paths = _init_into(tmpdir, mocker)

    assert _mode(paths["CONFIG_PATH"]) == 0o700
    for key in ("CLIENT_SECRETS_PATH", "SETTINGS_PATH"):
        mode = _mode(paths[key])
        assert mode == 0o600, f"{key} is {oct(mode)}"
        assert not mode & 0o077, f"{key} is accessible to group or others"


@requires_posix
def test_client_secret_permissions_are_not_inherited_from_the_source(tmpdir, mocker):
    """A permissive source file must not produce a permissive copy.

    shutil.copyfile does not carry permissions over, so the copy previously took whatever the umask
    allowed regardless of how the original was protected.
    """
    os.umask(0o022)
    paths = _init_into(tmpdir, mocker, source_mode=0o644)

    assert _mode(paths["CLIENT_SECRETS_PATH"]) == 0o600


@requires_posix
def test_existing_config_directory_is_tightened(tmpdir, mocker):
    """A directory left behind by an older version gets its permissions corrected."""
    os.umask(0o022)
    config_path = tmpdir.mkdir(".config-old")
    os.chmod(str(config_path), 0o755)  # noqa: S103  - reproduces the vulnerable state

    client_secret_file = tmpdir.join("secrets.json")
    with open(client_secret_file, "w") as f:
        json.dump({"installed": {"client_secret": "x"}}, f)
    for name, value in {
        "CONFIG_PATH": str(config_path),
        "CLIENT_SECRETS_PATH": os.path.join(str(config_path), "client_secrets.json"),
        "SETTINGS_PATH": os.path.join(str(config_path), "settings.yaml"),
        "CREDENTIALS_PATH": os.path.join(str(config_path), "credentials.json"),
    }.items():
        mocker.patch.object(whatstk.utils.gdrive, name, value)
    mocker.patch("pydrive2.auth.GoogleAuth.CommandLineAuth", return_value=True)

    gdrive_init(client_secret_file)
    assert _mode(str(config_path)) == 0o700


@requires_posix
def test_refresh_token_is_tightened_after_auth(tmpdir, mocker):
    """credentials.json is written by pydrive2, so whatstk must lock it down afterwards."""
    os.umask(0o022)
    config_path = str(tmpdir.mkdir(".config-token"))
    credentials_path = os.path.join(config_path, "credentials.json")

    client_secret_file = tmpdir.join("secrets.json")
    with open(client_secret_file, "w") as f:
        json.dump({"installed": {"client_secret": "x"}}, f)
    for name, value in {
        "CONFIG_PATH": config_path,
        "CLIENT_SECRETS_PATH": os.path.join(config_path, "client_secrets.json"),
        "SETTINGS_PATH": os.path.join(config_path, "settings.yaml"),
        "CREDENTIALS_PATH": credentials_path,
    }.items():
        mocker.patch.object(whatstk.utils.gdrive, name, value)

    def _write_token() -> bool:
        with open(credentials_path, "w") as f:
            f.write("refresh-token")
        os.chmod(credentials_path, 0o644)  # simulate a permissive writer
        return True

    mocker.patch("pydrive2.auth.GoogleAuth.CommandLineAuth", side_effect=_write_token)

    gdrive_init(client_secret_file)
    assert _mode(credentials_path) == 0o600


def test_client_secret_content_survives_the_copy(tmpdir, mocker):
    """Tightening permissions must not change what is written."""
    paths = _init_into(tmpdir, mocker)
    with open(paths["CLIENT_SECRETS_PATH"]) as f:
        assert json.load(f) == {"installed": {"client_secret": "SUPERSECRET"}}


# --- #177: Google Drive is deprecated, FutureWarning in 0.9, removal in 1.0 ---------------------


def test_gdrive_init_warns_it_is_deprecated(tmpdir, mocker):
    with pytest.warns(FutureWarning, match="deprecated and will be removed in whatstk 1.0"):
        _init_into(tmpdir, mocker)


def test_loading_from_gdrive_warns_it_is_deprecated(mocker):
    mocker.patch("whatstk.utils.gdrive._check_gdrive_config", return_value=True)
    mocker.patch("pydrive2.auth.GoogleAuth", return_value=True)
    mocker.patch("pydrive2.files.GoogleDriveFile.FetchMetadata", return_value=True)
    mocker.patch("pydrive2.files.GoogleDriveFile.GetContentString", return_value="mock text")

    with pytest.warns(FutureWarning, match="deprecated and will be removed in whatstk 1.0"):
        _load_str_from_file_id("some-id")
