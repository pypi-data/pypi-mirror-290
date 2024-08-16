import subprocess
import os
import base64
import json
import boto3
import sys
import logging
import binascii
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def install_or_upgrade(package, extra_index_url=None):
    pip_args = ["install", package]

    if extra_index_url:
        pip_args.extend(["--extra-index-url", extra_index_url])

    subprocess.check_call([sys.executable, "-m", "pip"] + pip_args)


def install_fixeditcli(version: str = None, token_json: str = None):
    token_data = json.loads(token_json)

    # Extract AWS credentials and artifact domain from token data
    aws_access_key_id = token_data.get("key_id")
    aws_secret_access_key = token_data.get("key")
    aws_region = token_data.get("region")
    artifact_domain = token_data.get("py_domain")
    py_repository = token_data.get("py_repository")

    if not (aws_access_key_id and aws_secret_access_key and aws_region):
        raise ValueError("AWS credentials not found in token data.")

    # Fetch AWS account ID
    account_id = (
        boto3.client(
            "sts",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
        .get_caller_identity()
        .get("Account")
    )

    # Get CodeArtifact authorization token
    codeartifact_auth_token = (
        boto3.client(
            "codeartifact",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
        .get_authorization_token(domain=artifact_domain, domainOwner=account_id)
        .get("authorizationToken")
    )

    # Set up index URL
    index_url = f"https://aws:{codeartifact_auth_token}@{artifact_domain}-{account_id}.d.codeartifact.{aws_region}.amazonaws.com/pypi/{py_repository}/simple/"

    # Determine fixeditcli package version
    fixeditcli_package = f"fixeditcli=={version}"

    # Install or upgrade fixeditcli package
    install_or_upgrade(fixeditcli_package, extra_index_url=index_url)


#-----------------Entry Point Functions-----------------#
def read_version_entry():
    """Read the FixedIT CLI version from the env variable only."""
    if os.getenv("FIXEDITCLI_VERSION"):
        return os.getenv("FIXEDITCLI_VERSION")
    else:
        raise ValueError(
            "FIXEDITCLI_VERSION environment variable must be set before running the installer from "
            "an entrypoint."
        )
    

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


def fixeditcli_install_entry():
    """Install the FixedIT CLI using the FixedIT token entrypoint
       function."""
    try:
        token = get_fixedit_token()
        version = read_version_entry()
        token_json = decode_token(token)
        update_config(token)

        install_fixeditcli(version, token_json)
    except Exception as e:
        logger.error(f"Failed to install FixedIT CLI: {e}")
        raise e