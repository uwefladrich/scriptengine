from se.tasks import Copy
from se.jobs import Job
from se.scripts import SimpleScriptEngine


config = {  'common': {
                'srcdir': '/foo',
                'rundir': 'bar-{{item}}/',
                'n': 3
            },
            'ifs': {
                'executable': '{{common.srcdir}}/ifs/ifsmaster.exe'
            },
            'nemo': {
                'config': 'ORCA1L75',
                'executable': '{{common.srcdir}}/nemo/CONFIG/{{nemo.config}}/nemo.exe'
            },
         }

copy_executable_job = Job()

copy_executable_job.append( Copy({ 'src': '{{nemo.executable}}', 'dst': '{{common.rundir}}' }) )
copy_executable_job.append( Copy({ 'src': '{{ifs.executable}}',  'dst': '{{common.rundir}}' }) )

copy_executable_job.when = '{{common.n}} < 4'
copy_executable_job.loop = [ 'a', 'b', 'c' ]

SimpleScriptEngine().run(jobs=[copy_executable_job], **config, dryrun=True)
