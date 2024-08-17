import sys
import os
import logging


class StoppingCondition:
    def __init__(self, path, stopfile, stopmagic) -> None:
        self.path = path
        self.stopfile = stopfile
        self.stopmagic = stopmagic

    def check_magic(self):
        with open(self.get_stop_path(), "r") as f:
            for line in f:
                if self.stopmagic in line:
                    return True
        return False

    def get_stop_path(self):
        return self.path + "/" + self.stopfile

    def eval(self):
        if self.stopfile is not None:

            fpath = self.get_stop_path()
            if os.path.exists(fpath) and self.stopmagic == "":
                logging.info(f"exit because file {fpath} is present.")
                sys.exit(1)

            if os.path.exists(fpath) and self.check_magic():
                logging.info(
                    f"""exit because file {fpath}
                     contains magic {self.stopmagic}"""
                )
                sys.exit(1)
