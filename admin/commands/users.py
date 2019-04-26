import os
import shutil

from cliff.command import Command
from cliff.lister import Lister

import owncloud_utils.crypto as cryp
import owncloud_utils.strings as stru
from constants import constants
from database.models import Users
from database.repositories import UserRepository


class ListUsers(Lister):
    """Displays the list of all registered users"""

    def take_action(self, parsed_args):
        repo = UserRepository.get_instance()

        users_list = repo.all()

        print(f"{len(users_list)} records")

        return (
            ("ID", "Username", "Storage Limit (bytes)"),
            ((user.id, user.username, user.storage_limit)
             for user in users_list)
        )


class AddUser(Command):

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument("username", help="Unique username")

        return parser

    def take_action(self, parsed_args):
        repo = UserRepository.get_instance()

        username = parsed_args.username
        user = repo.get_by_username(username)

        if user:
            raise ValueError(f"{username} is not allowed")

        generated_password = stru.randstr(len=8)

        user = Users()
        user.username = username
        user.password = cryp.digest_string(generated_password)

        repo.create(user)

        user_dir = f"{constants.work_dir()}/{user.username}/_user"
        os.makedirs(user_dir)

        print(f"{username} created. Generated password: {generated_password}")


class DeleteUser(Command):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "username", help="Unique name of the user to delete")

        return parser

    def take_action(self, parsed_args):
        repo = UserRepository.get_instance()

        username = parsed_args.username
        user = repo.get_by_username(username)

        if not user:
            raise ValueError(f"{username} is invalid")

        repo.delete(user)

        user_dir = f"{constants.work_dir()}/{user.username}"
        shutil.rmtree(user_dir)

        print(f"{username} deleted")
