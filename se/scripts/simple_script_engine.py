""" SimpleScriptEngine for ScriptEngine.

SimpleScriptEngine is a simplistic script engine. It runs all jobs sequentially
on the local machine, without consideration of job contexts.
"""

from deepmerge import always_merger

class SimpleScriptEngine:
    """Simplistic script engine for ScriptEngine.

    This script engine's main routine, run(), takes a list of jobs (the script)
    and runs the jobs sequentially by calling their run() method.
    """

    def run(self, *, dryrun=False, script=[]):
        """Run joblist (script) one-by-one.

        Takes care of the configuration dicts that jobs may return by providing
        and updating the global configuration.

        Note that the configuration update needs a deep directory update. This
        is because partial updates may delete the configuration otherwise. For
        example, if the configuration:

        - config:
            foo:
                bar: 1
                baz: 2

        is updated with:

        - config:
            foo:
                baz: 3

        a normal dict.update() call would remove foo.bar.
        """
        config = {}
        for job in script:
            config_update = job.run(dryrun=dryrun, **config)
            if config_update is not None:
                always_merger.merge(config, config_update)
