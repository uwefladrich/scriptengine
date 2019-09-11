"""SlurmSubmit task for ScriptEngine."""

import os
import subprocess

from se.tasks import Task
from se.helpers import render_string
from se.exceptions import ScriptEngineStopException


class SlurmSubmit(Task):
    """SlurmSubmit task, submits a script to the SLURM batch system
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["account",
                                                                    "nodes",
                                                                    "time",
                                                                    "scripts"])

    def __str__(self):
        return f"SlurmSubmit: ..."

    def run(self, context):

        if os.environ.get("SLURM_JOB_NAME"):
            context[getattr(self, "set_context", None) or "slurm"] = True
            return

        batch_cmd = ["sbatch", f"--account={self.account}",
                               f"--nodes={self.nodes}",
                               f"--time={self.time}"]
        batch_cmd.extend(getattr(self, "sbatch_args", []))
        batch_cmd.append("se")
        batch_cmd.extend(self.scripts)

        self.log_info("Submit ScriptEngine job to SLURM")
        self.log_debug(batch_cmd)

        subprocess.run(map(str, batch_cmd))
        raise ScriptEngineStopException("SlurmSubmit task requests stop after submitting batch job")
