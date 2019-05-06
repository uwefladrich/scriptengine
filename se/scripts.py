from deepmerge import always_merger

class SimpleScriptEngine(object):

    def run(self, *, dryrun=False, script=[]):
        config = {}
        for job in script:
            cfg = job.run(dryrun=dryrun, **config)
            if cfg is not None:
                always_merger.merge(config, cfg)
