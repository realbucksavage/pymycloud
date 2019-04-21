import os
import uuid

from cliff.command import Command
from cliff.lister import Lister

import owncloud_utils.crypto as cryp
import owncloud_utils.strings as stru
from database.models import Users
from database.session import SessionFactoryPool


class ListUsers(Lister):
    "Displays the list of all registered users"

    def take_action(self, parsed_args):
        database_session = SessionFactoryPool.get_current_session()

        users_list = database_session.query(Users).all()

        print(f"{database_session.query(Users).count()} recods")

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
        database_session = SessionFactoryPool.get_current_session()

        username = parsed_args.username
        user = database_session.query(Users).filter(
            Users.username == username).first()

        if user:
            raise ValueError(f"{username} is not allowed")

        generated_password = stru.randstr(len=8)

        user = Users()
        user.username = username
        user.password = cryp.digest_string(generated_password)

        database_session.add(user)
        database_session.commit()

        print(f"{username} created. Generated password: {generated_password}")


class DeleteUser(Command):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "username", help="Unique name of the user to delete")

        return parser

    def take_action(self, parsed_args):
        database_session = SessionFactoryPool.get_current_session()

        username = parsed_args.username
        user = database_session.query(Users).filter(
            Users.username == username).first()

        if not user:
            raise ValueError(f"{username} is invalid")

        database_session.delete(user)
        database_session.commit()

        print(f"{username} deleted")
