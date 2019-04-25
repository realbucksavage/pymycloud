import os


class Const:
    def work_dir(self):
        path_in_var = os.environ.get("PYMYCLOUD_HOME")
        return path_in_var if path_in_var else "/pymycloud"


constants = Const()
