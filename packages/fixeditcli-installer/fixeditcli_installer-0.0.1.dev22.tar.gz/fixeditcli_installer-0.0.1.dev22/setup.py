from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class install_wrapper(_install):
    """Custom install command wrapper for FixedIT CLI installation.
    This wrapper will not attempt to install the FixedIT CLI if
    the FIXEDIT_TOKEN environment variable is not set and will log a warning
    instead. This is to prevent the FixedIT CLI from being installed in
    gitlab CI/CD pipelines where the token is not available or we do not
    want to install the FixedIT CLI but just build the package."""

    def _install_fixeditcli(self):
        try:
            from fixeditcli_installer.src.installer import install_fixeditcli, update_config, decode_token, read_version, get_fixedit_token

            token = get_fixedit_token()
            version = read_version()
            token_json = decode_token(token)
            update_config(token)

            install_fixeditcli(version, token_json)
        except Exception as e:
            logger.error(f"Failed to install FixedIT CLI: {e}")
            raise e

    def run(self):
        # Install the FixedIT CLI Installer package
        _install.run(self)

        # Only run post-installation tasks if running in an install context
        # Post-instalation tasks include installing the FixedIT CLI, setting up
        # the ~/.fixedit config file and reading the FixedIT CLI version from the
        # version.txt file.
        if os.getenv("FIXEDIT_TOKEN"):
            self._install_fixeditcli()
        else:
            logger.warning(
                "FIXEDIT_TOKEN environment variable not set. Skipping FixedIT CLI installation. \n"
                "If you want to install the FixedIT CLI, make sure to set the FIXED_TOKEN environment "
                "variable before running the installer."
            )

setup(
    name="fixeditcli_installer",
    version="0.0.1_dev22",
    package_dir={"": "src"},
    packages=find_packages("src"),
    py_modules=["src/installer"],
    entry_points={
        'console_scripts': [
            'fixeditcli-install=installer:entry'
        ]
    },
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
)