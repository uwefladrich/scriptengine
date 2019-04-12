class SimpleScriptEngine(object):

    def run(self, *, dryrun=False, jobs=[], **config):
        for job in jobs:
            job.run(dryrun=dryrun, **config)
