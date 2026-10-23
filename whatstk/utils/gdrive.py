"""Google Drive utils.

.. deprecated:: 0.9.0

    Google Drive support is deprecated and will be removed in 0.10.0. Download the export and pass
    a local path instead. See `issue #177 <https://github.com/lucasrodes/whatstk/issues/177>`_.

.. warning::

    To load chats from google drive, install the library with the corresponding extension (ignore the
    ``--upgrade`` option if you haven't installed the library):

    .. code-block::

        pip install whatstk[gdrive] --upgrade
"""

import os
import warnings

try:
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    from pydrive2.files import ApiRequestError
    import yaml
except ImportError as e:  # pragma: no cover
    msg = (  # pragma: no cover
        "whatstk Google Drive requirements are not installed.\n\n"
        "Please pip install as follows:\n\n"
        '  python -m pip install "whatstk[gdrive]" --upgrade  # or python -m pip install'
    )  # pragma: no cover
    raise ImportError(msg) from e  # pragma: no cover


# Create .config/whatstk/gdrive if it does not exist
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "whatstk", "gdrive")
CLIENT_SECRETS_PATH = os.path.join(CONFIG_PATH, "client_secrets.json")
SETTINGS_PATH = os.path.join(CONFIG_PATH, "settings.yaml")
CREDENTIALS_PATH = os.path.join(CONFIG_PATH, "credentials.json")

# This directory holds the OAuth client secret and the refresh token, so nothing in it should be
# readable by other users of the machine. POSIX only: on Windows these bits are largely ignored.
CONFIG_DIR_MODE = 0o700
CREDENTIAL_FILE_MODE = 0o600

_DEPRECATION_MESSAGE = (
    "Google Drive support is deprecated and will be removed in whatstk 0.10.0. Download the export "
    "and pass a local path to df_from_whatsapp or WhatsAppChat.from_source instead. See "
    "https://github.com/lucasrodes/whatstk/issues/177"
)


def _warn_deprecated() -> None:
    """Emit the Google Drive deprecation warning."""
    warnings.warn(_DEPRECATION_MESSAGE, FutureWarning, stacklevel=3)


def _write_private(path: str, data: bytes) -> None:
    """Write ``data`` to ``path``, readable and writable only by the current user.

    The mode is passed to ``os.open`` rather than applied afterwards with ``chmod``, so the file is
    never briefly world-readable. An existing file keeps its old mode through ``O_TRUNC``, hence the
    explicit ``chmod`` as well.

    Args:
        path (str): Destination path.
        data (bytes): Content to write.
    """
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, CREDENTIAL_FILE_MODE)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.chmod(path, CREDENTIAL_FILE_MODE)


def gdrive_init(client_secret_file: str, encoding: str = "utf8") -> None:
    """Initialize GDrive credentials.

    This should only run once before reading a file from Google Drive the first time. Subsequent executions should run
    seamlessly.

    To obtain `client_secret_file`, follow the instructions from:
    https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20

    The client secret, the generated settings and the refresh token are written to
    ``~/.config/whatstk/gdrive`` with permissions ``0600``, inside a directory with ``0700``, so that
    other users of the machine cannot read them. These are POSIX permission bits; Windows largely
    ignores them, so on Windows the files are only as protected as the user's profile directory.

    Notes:
        - Additionally, make sure to add yourself in Test users, as noted in:
          https://stackoverflow.com/questions/65980758/pydrive-quickstart-and-error-403-access-denied
        - Select Desktop App instead of Web Application as the application type.

    Args:
        client_secret_file (str): Path to clien_secret.json file (Created in Google Console).
        encoding (str): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.
    """
    _warn_deprecated()

    os.makedirs(CONFIG_PATH, mode=CONFIG_DIR_MODE, exist_ok=True)
    # makedirs only applies the mode to directories it creates, and subtracts the umask, so set it
    # explicitly to also tighten a directory left behind by an earlier version.
    os.chmod(CONFIG_PATH, CONFIG_DIR_MODE)

    # Copy credentials to config folder. Read and rewrite rather than shutil.copyfile, which does
    # not carry permissions over and would leave the copy at whatever the umask allows.
    with open(client_secret_file, "rb") as f:
        _write_private(CLIENT_SECRETS_PATH, f.read())

    # Create settings.yaml file
    dix = {
        "client_config_backend": "file",
        "client_config_file": CLIENT_SECRETS_PATH,
        "save_credentials": True,
        "save_credentials_backend": "file",
        "save_credentials_file": CREDENTIALS_PATH,
        "get_refresh_token": True,
        "oauth_scope": [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.install",
        ],
    }
    _write_private(SETTINGS_PATH, yaml.dump(dix).encode(encoding))

    # credentials.json
    gauth = GoogleAuth(settings_file=SETTINGS_PATH)
    gauth.CommandLineAuth()
    # The refresh token is written by pydrive2, so tighten it once it exists.
    if os.path.isfile(CREDENTIALS_PATH):
        os.chmod(CREDENTIALS_PATH, CREDENTIAL_FILE_MODE)


def _check_gdrive_config() -> None:
    error_msg = (
        "Google Drive not correctly configured. Run `gdrive_init(client_secret_file)` (from whatstk.utils.gdrive)."
    )
    if not os.path.isdir(CONFIG_PATH):
        raise ValueError(error_msg)
    for f in [CLIENT_SECRETS_PATH, SETTINGS_PATH]:
        if not os.path.isfile(f):
            raise ValueError(error_msg)


def _load_str_from_file_id(file_id: str) -> str:
    _warn_deprecated()
    _check_gdrive_config()
    gauth = GoogleAuth(settings_file=SETTINGS_PATH)
    drive = GoogleDrive(gauth)
    # Load file using id
    try:
        file_obj = drive.CreateFile({"id": file_id})
        file_obj.FetchMetadata()
    except ApiRequestError as err:
        raise ValueError(
            f"File ID {file_id} not valid. Please use a valid File ID. You can find it in the shareable file link."
        ) from err
    # Get raw file content as str
    txt = file_obj.GetContentString()
    return txt
