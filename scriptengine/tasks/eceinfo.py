"""ScriptEngine tasks for handling the EC-Earth ece.info file
"""

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render

# #
# # Finished leg at 2019-01-07 14:45:20 after 01:59:13 (hh:mm:ss)
# # CPMIP performance: 12.07 SYPD   1559 CHPSY
# leg_number=1
# leg_start_date="Tue, 01 Jan 1850 00:00:00 +0000"
# leg_end_date="Wed, 01 Jan 1851 00:00:00 +0000"


class UpdateEceinfo(Task):
    """ScriptEngine UpdateEceinfo task: reads an EC-Earth ece.info file and
    updates information in context
    """
    def __init__(self, parameters):
        super().__init__(__name__+".update", parameters, required_parameters=["path"])

    def run(self, context):
        eceinfo_path = j2render(self.path, context)
        self.log_info(f"Updating eceinfo from {eceinfo_path}")

        eceinfo_in_file = {}
        try:
            with open(eceinfo_path) as file:
                self.log_debug("Found ece.info file, reading values")
                for line in file:
                    line_without_comment = line.split("#")[0]
                    key, value = line_without_comment.partition("=")[::2]
                    eceinfo_in_file[key.strip()] = value.strip()
        except FileNotFoundError:
            self.log_warning(f"No ece.info file found at '{eceinfo_path}', assuming new run")

        eceinfo_in_context = context.setdefault("eceinfo", {})
        eceinfo_in_context["leg"] = int(eceinfo_in_file.get("leg", 0)) + 1


class WriteEceinfo(Task):
    """ScriptEngine WriteEceinfo task: writes present eceinfo from context to file
    """
    def __init__(self, parameters):
        super().__init__(__name__+".write", parameters, required_parameters=["path"])

    def run(self, context):
        eceinfo_path = j2render(self.path, context)
        self.log_info(f"Wrinting eceinfo to {eceinfo_path}")
        if "eceinfo" in context:
            self.log_debug(f"Attempt to write eceinfo to {eceinfo_path}")
            with open(eceinfo_path, "a+") as file:
                file.write("# ---\n")
                for key, value in context["eceinfo"].items():
                    file.write(f"{key}={value}\n")
            self.log_debug(f"Writing eceinfo to {eceinfo_path} completed")
        else:
            self.log_warning("No eceinfo in context, file not updated!")
