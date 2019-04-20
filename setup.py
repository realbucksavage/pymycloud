from setuptools import setup, find_packages

setup(
    name="owncloud_admin",
    description="Utility to manage the OwnCloud installation",
    version="0.1-beta",
    author="Jay Godara",
    entry_points={
        "console_scripts": [
            "owncloud_admin = owncloud_admin:main"
        ]
    }
)
