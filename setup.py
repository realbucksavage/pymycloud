from setuptools import find_packages, setup

setup(
    name="owncloud_admin",
    description="Utility to manage the OwnCloud installation",
    version="0.1-beta",
    author="Jay Godara",
    entry_points={
        "console_scripts": [
            "owncloud_admin = admin.owncloud_admin:main"
        ]
    }
)
