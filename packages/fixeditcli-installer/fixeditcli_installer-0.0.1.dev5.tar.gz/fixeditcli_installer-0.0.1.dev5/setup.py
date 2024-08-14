from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from pathlib import Path
import binascii
import base64
import os
import json
import logging

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


def read_version():
    """Read the FixedIT CLI version from the version text file."""
    if os.getenv("FIXEDITCLI_VERSION"):
        return os.getenv("FIXEDITCLI_VERSION")

    here = Path(__file__).resolve().parent
    version_file = here / "version.txt"
    try:
        with open(version_file, "r") as f:
            version = f.read().strip()
    except IOError as e:
        raise ValueError(
            "Could not read the version file. Make sure that the version file is present in the "
            "same directory as the setup.py file."
        ) from e
    return version


def _install_fixeditcli(self):
    try:
        token = get_fixedit_token()
        version = read_version()
        token_json = decode_token(token)
        update_config(token)

        from src.installer import install_fixeditcli

        install_fixeditcli(version, token_json)
    except Exception as e:
        logger.error(f"Failed to install FixedIT CLI: {e}")
        raise

class install_wrapper(_install):
    """Custom install command wrapper for FixedIT CLI installation.
    This wrapper will not attempt to install the FixedIT CLI if
    the FIXEDIT_TOKEN environment variable is not set and will log a warning
    instead. This is to prevent the FixedIT CLI from being installed in
    gitlab CI/CD pipelines where the token is not available or we do not
    want to install the FixedIT CLI but just build the package."""

    def run(self):
        # Install the FixedIT CLI Installer package
        _install.run(self)

        # Only run post-installation tasks if running in an install context
        # Post-instalation tasks include installing the FixedIT CLI, setting up
        # the ~/.fixedit config file and reading the FixedIT CLI version from the
        # version.txt file.
        if os.getenv("FIXEDIT_TOKEN"):
            _install_fixeditcli()
        else:
            logger.warning(
                "FIXEDIT_TOKEN environment variable not set. Skipping FixedIT CLI installation. \n"
                "If you want to install the FixedIT CLI, make sure to set the FIXED_TOKEN environment "
                "variable before running the installer."
            )

setup(
    name="fixeditcli_installer",
    version="0.0.1_dev_5",
    package_dir={"": "src"},
    packages=find_packages("src"),
    py_modules=['entrypoints'],
    include_package_data=True,
    python_requires=">=3.8",
    author="FixedIT Consulting AB",
    license="proprietary",
    keywords="acap axis camera",
    url="https://fixedit.ai",
    author_email="info@fixedit.ai",
    description="Installer for FixedIT CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={"install": install_wrapper},
    entry_points={
        'console_scripts': [
            'fixeditcli-install=entrypoints.fixeditcli_install:main'
        ]
    },
)