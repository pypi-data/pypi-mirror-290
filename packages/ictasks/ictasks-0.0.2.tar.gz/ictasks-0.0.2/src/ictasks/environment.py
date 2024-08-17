import uuid
import logging

from icsystemutils.cluster.node import ComputeNode

from .scheduler.schedulers.slurm import SlurmJob

logger = logging.getLogger(__name__)


class Environment:
    def __init__(self) -> None:
        self.job_id: str | None = None
        self.nodelist: list[ComputeNode] = []


class BasicEnvironment(Environment):
    def __init__(self, job_id: str | None = None, nodelist: list[str] = []) -> None:
        super().__init__()

        if not job_id:
            self.job_id = str(uuid.uuid4())
        else:
            self.job_id = job_id

        if not nodelist:
            self.nodelist = [ComputeNode("localhost")]
        else:
            self.nodelist = [ComputeNode(a) for a in nodelist]


class SlurmEnvironment(Environment):
    def __init__(self) -> None:
        super().__init__()
        self.slurm_job = SlurmJob()
        self.nodelist = [ComputeNode(a) for a in self.slurm_job.nodes]

    @staticmethod
    def detect() -> bool:
        return bool(SlurmJob.get_id())


def autodetect_environment() -> Environment:
    if SlurmEnvironment.detect():
        logger.info("Detected we are running in a slurm environment")
        return SlurmEnvironment()
    else:
        logger.info("No runtime environment recognized - using basic environment")
        return BasicEnvironment()
