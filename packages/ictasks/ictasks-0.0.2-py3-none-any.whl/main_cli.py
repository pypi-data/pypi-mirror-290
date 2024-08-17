import os
from pathlib import Path
import sys
import signal
import argparse
import logging

from iccore import logging_utils
from ictasks.session import Session
from ictasks.environment import (
    Environment,
    SlurmEnvironment,
    BasicEnvironment,
    autodetect_environment,
)


logger = logging.getLogger(__name__)


def kill_all(signum, stack):

    """
    Signal handler for SIGINT
    """

    logger.info("Session interrupted. Please check for orphaned processes.")
    sys.exit(1)


def main_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory to run the session in",
    )
    parser.add_argument("--tasklist", type=Path, help="Path to tasklist file")
    parser.add_argument("--nodelist", type=str, help="List of system nodes")
    parser.add_argument("--jobid", type=str, help="Identifier for this job")
    parser.add_argument(
        "--env", type=str, help="Environment to run the session in, 'slurm' or 'basic'"
    )

    args = parser.parse_args()

    logging_utils.setup_default_logger()

    signal.signal(signal.SIGINT, kill_all)

    env: Environment | None = None
    if args.env == "slurm":
        logger.info("Running in slurm environment")
        env = SlurmEnvironment()
    elif args.env == "basic":
        logger.info("Running in basic environment")
        env = BasicEnvironment(args.job_id, args.nodelist.split(","))
    else:
        logger.info("Trying to detect runtime environment")
        env = autodetect_environment()

    session = Session(args.work_dir, env, args.tasklist)
    logger.info("Starting session run")
    session.run()
    logger.info("Finished session run")


if __name__ == "__main__":
    main_cli()
