import subprocess
import os
import base64
import json
import boto3
import sys
import pathlib


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
