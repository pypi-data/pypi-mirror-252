"""
Main CLI entrypoint.
"""

import sys


def print_info() -> None:
    """
    Print package info to stdout.
    """
    print(
        "Type annotations for aiobotocore.Pinpoint 2.11.0\nVersion:         2.11.0\nBuilder"
        " version: 7.23.1\nDocs:           "
        " https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint//\nBoto3"
        " docs:     "
        " https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint\nOther"
        " services:  https://pypi.org/project/boto3-stubs/\nChangelog:      "
        " https://github.com/youtype/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    """
    Print package version to stdout.
    """
    print("2.11.0")


def main() -> None:
    """
    Main CLI entrypoint.
    """
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
