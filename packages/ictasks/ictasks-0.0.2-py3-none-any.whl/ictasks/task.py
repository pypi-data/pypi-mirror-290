class Task:
    def __init__(self, id, launch_cmd, extra_paths=[]) -> None:
        self.id = id
        self.launch_cmd = launch_cmd
        self.extra_paths = extra_paths
