import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from admin.commands.users import AddUser, DeleteUser, ListUsers
from database.session import SessionFactoryPool


class OwnCloudAdmin(App):

    def __init__(self):
        super().__init__(
            description="Utility to manage the OwnCloud installation",
            version="0.1-beta",
            command_manager=CommandManager("owncloud_admin"),
            deferred_help=True
        )

    def prepare_to_run_command(self, cmd):
        # Initialze the database session
        _ = SessionFactoryPool.get_current_session()

    def initialize_app(self, argv):
        commands = [ListUsers, AddUser, DeleteUser]
        for command in commands:
            self.command_manager.add_command(
                command.__name__.lower(), command)


def main(argv=sys.argv[1:]):
    admin_app = OwnCloudAdmin()
    return admin_app.run(argv)


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv[1:]))
