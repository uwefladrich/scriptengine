from se.tasks import Task


class Command(Task):

    def __init__(self, dict):
        super(Command, self).__init__(dict, 'name')

        if 'args' not in self.__dict__:
            self.args = []
        else:
            # Assert args is a list
            pass

    def __str__(self):
        return 'Running command "{}" with argument list "{}"'.format(self.name, self.args)

    def run(self):
        print(self)
