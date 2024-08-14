from pathlib import Path
import binascii
import base64
import os
import json
import logging
import pkg_resources

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_fixedit_token():
    """Get the FixedIT token from the environment variables."""
    fixedit_token = os.getenv("FIXEDIT_TOKEN")
    if not fixedit_token:
        raise EnvironmentError(
            "FIXEDIT_TOKEN environment variable must be set before running the installer."
        )
    return fixedit_token


def decode_token(token):
    """Decode the FixedIT token from base64 to JSON."""
    try:
        token_json = base64.b64decode(token).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as e:
        raise ValueError(
            "The FIXEDIT_TOKEN you have specified is not a correctly formatted key. Make "
            "sure you have generated it correctly and copied the whole string when setting "
            "it as an environment variable."
        ) from e
    return token_json

def update_config(token):
    config_path = Path.home() / ".fixedit"
    tmp_config_path = Path.home() / ".fixedit.tmp"

    try:
        config_data = config_path.read_text()
        config_data = json.loads(config_data)
    except FileNotFoundError:
        config_data = {}

    overwrite_env = os.getenv("FIXEDIT_TOKEN_OVERWRITE")
    overwrite = overwrite_env == "1" if overwrite_env else False

    if not config_data:
        config_data["secrets"] = {"default": token}
    elif overwrite:
        # Handle corrupted config files case (Missing secrets key)
        try:
            config_data["secrets"]["default"] = token
        except KeyError:
            logger.warning(
                "Config file exists but token to overwrite is missingin the ~.fixedit "
                "config file. Writing the new token..."
            )
            config_data["secrets"] = {"default": token}

    with tmp_config_path.open("w") as f_new:
        json.dump(config_data, f_new, indent=4)

    tmp_config_path.rename(config_path)


def read_version_entry():
    """Read the FixedIT CLI version from the version text file."""
    if os.getenv("FIXEDITCLI_VERSION"):
        return os.getenv("FIXEDITCLI_VERSION")
    else:
        raise ValueError(
            "FIXEDITCLI_VERSION environment variable must be set before running the installer from "
            "an entrypoint."
        )

def fixeditcli_install_fnc():
    """Install the FixedIT CLI using the FixedIT token entrypoint
       function."""
    try:
        token = get_fixedit_token()
        version = read_version_entry()
        token_json = decode_token(token)
        update_config(token)

        from ..installer import install_fixeditcli

        install_fixeditcli(version, token_json)
    except Exception as e:
        logger.error(f"Failed to install FixedIT CLI: {e}")
        raise e
    
def main():
    fixeditcli_install_fnc()
