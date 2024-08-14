class BaseRunner:

    def __init__(self) -> None:
        self.tasks = list()

    def add_task(self, func, *args, **kwargs):
        self.tasks.append((func, args, kwargs))

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
