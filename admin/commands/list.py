from cliff.lister import Lister
import os


class ListUsers(Lister):
    "Displays the list of all registered users"

    def take_action(self, parsed_args):
        return (('Name',),
                ((n,) for n in range(10))
                )
