import sys
import json

from .linux_cpu import ProcInfoReader
from .mac_cpu import SysctlCpuReader


class CpuInfo:
    """Class to read and store system cpu information

    Attributes:
        physical_procs (dict): Collection of physical processor info
        threads_per_core (:obj:`int`): Number of threads available per processor core
        cores_per_node (:obj:`int`): Number of cores per compute node (network location)
    """

    def __init__(
        self,
    ) -> None:
        self.physical_procs: dict = {}
        self.threads_per_core = 1
        self.cores_per_node = 1

        if sys.platform == "darwin":
            self.reader = SysctlCpuReader()
        else:
            self.reader = ProcInfoReader()

        self.read()

    def read(self):
        """Read the processor information from the system."""
        self.reader.read()
        self._refresh()

    def _refresh(self):
        if not self.physical_procs:
            return

        # This is assuming all processors have same number of cores
        # and all cores have same number of threads
        self.cores_per_node = len(self.physical_procs.values()[0].cores)
        self.threads_per_core = len(
            self.physical_procs.values()[0].cores.values()[0].threads
        )

    def serialize(self) -> dict:
        return {
            "physical_procs": [p.serialize() for p in self.physical_procs],
            "threads_per_core": self.threads_per_core,
            "cores_per_node": self.cores_per_node,
        }

    def __str__(self) -> str:
        return json.dumps(self.serialize())
