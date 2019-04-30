class SimpleScriptEngine(object):

    def run(self, *, dryrun=False, script=[], **config):
        for job in script:
            job.run(dryrun=dryrun, **config)
