"""Google Drive utils.

.. warning::

    To load chats from google drive, install the library with the corresponding extension (ignore the
    ``--upgrade`` option if you haven't installed the library):

    .. code-block::

        pip install whatstk[gdrive] --upgrade
"""


from shutil import copyfile
import os

try:
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    from pydrive2.files import ApiRequestError
    import yaml
except ImportError as e:
    msg = (
        "whatstk Google Drive requirements are not installed.\n\n"
        "Please pip install as follows:\n\n"
        '  python -m pip install "whatstk[gdrive]" --upgrade  # or python -m pip install'
    )
    raise ImportError(msg) from e


# Create .config/whatstk/gdrive if it does not exist
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "whatstk", "gdrive")
CLIENT_SECRETS_PATH = os.path.join(CONFIG_PATH, "client_secrets.json")
SETTINGS_PATH = os.path.join(CONFIG_PATH, "settings.yaml")
CREDENTIALS_PATH = os.path.join(CONFIG_PATH, "credentials.json")


def gdrive_init(client_secret_file: str, encoding: str = "utf8") -> None:
    """Initialize GDrive credentials.

    This should only run once before reading a file from Google Drive the first time. Subsequent executions should run
    seamlessly.

    To obtain `client_secret_file`, follow the instructions from:
    https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20

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
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH, exist_ok=True)

    # Copy credentials to config folder
    copyfile(client_secret_file, CLIENT_SECRETS_PATH)

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
    with open(SETTINGS_PATH, "w", encoding=encoding) as f:
        yaml.dump(dix, f)

    # credentials.json
    gauth = GoogleAuth(settings_file=SETTINGS_PATH)
    gauth.CommandLineAuth()


def _check_gdrive_config() -> None:
    error_msg = (
        "Google Drive not correctly configured. Run `gdrive_init(client_secret_file)` (from whatstk.utils.gdrive)."
    )
    if not os.path.isdir(CONFIG_PATH):
        raise ValueError(error_msg)
    for f in [CLIENT_SECRETS_PATH, SETTINGS_PATH]:
        if not os.path.isfile(f):
            raise ValueError(error_msg)


def _load_str_from_file_id(file_id: int) -> str:
    _check_gdrive_config()
    gauth = GoogleAuth(settings_file=SETTINGS_PATH)
    drive = GoogleDrive(gauth)
    # Load file using id
    try:
        file_obj = drive.CreateFile({"id": file_id})
        file_obj.FetchMetadata()
    except ApiRequestError:
        raise ValueError(
            f"File ID {file_id} not valid. Please use a valid File ID. You can find it in the shareable file link."
        )
    # Get raw file content as str
    txt = file_obj.GetContentString()
    return txt
