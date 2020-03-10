"""SLURM Sbatch task for ScriptEngine."""

import os
import subprocess

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render
from scriptengine.exceptions import ScriptEngineStopException


class Sbatch(Task):
    """Sbatch task, submits SE scripts to the SLURM batch system
    """

    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["se_scripts"])

    def run(self, context):

        if os.environ.get("SLURM_JOB_NAME"):
            context[getattr(self, "set_context", None) or "slurm"] = True
            return

        opt_args = []
        for opt, arg in self.__dict__.items():
            if opt == "se_scripts":
                if isinstance(arg, list):
                    scripts = [j2render(script, context) for script in arg]
                else:
                    scripts = [j2render(arg, context)]
            elif not opt.startswith("_"):
                opt_args.append(f"--{opt}")
                if arg:
                    opt_args.append(j2render(arg, context))

        sbatch_cmd = ["sbatch"]
        sbatch_cmd.extend(map(str, opt_args))
        sbatch_cmd.append("se")
        sbatch_cmd.extend(map(str, scripts))

        self.log_debug(f"{sbatch_cmd}")

        try:
            subprocess.run(sbatch_cmd, check=True)
        except subprocess.CalledProcessError:
            self.log_error("Sbatch command returns an error")
            raise
        else:
            raise ScriptEngineStopException("Sbatch task requests stop "
                                            "after submitting batch job")
