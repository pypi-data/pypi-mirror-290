from git import Repo
from dotenv import dotenv_values

fname_config = ".git_monitor"


class Monitor:

    def __init__(self, path_proj, name):
        self.repo = Repo(path_proj)
        self.name = name

    @classmethod
    def by_env(cls, name):
        config = dotenv_values(fname_config)
        if name in config:
            try:
                monitor = cls(config[name], name)
                monitor.print_status()
            except Exception as e:
                print(e)
            return monitor

    def print_status(self):

        print(f"Project {self.name} status:\n")

        if self.repo.head.is_detached:
            print("On Detached head.")
        else:
            print(f"On branch {self.repo.active_branch}.")

        print(f"Current commit- {self.repo.head.object.hexsha}")
        print(f"Message-\n{self.repo.head.commit.message}")

        if len(self.repo.untracked_files) > 0:
            print("\nuntracked-")
            for file in self.repo.untracked_files:
                print(file)

        diffs = self.repo.index.diff(None)
        if len(diffs) > 0:
            print("\nmodified-")
            for d in diffs:
                print(d.a_path)

        print("\n")
