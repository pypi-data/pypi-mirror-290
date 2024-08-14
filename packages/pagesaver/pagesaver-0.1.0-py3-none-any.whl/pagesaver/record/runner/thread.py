import threading

from pagesaver.record.runner.base import BaseRunner


class BackgroundThreadRunner(BaseRunner):
    def __init__(self) -> None:
        super().__init__()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True

    def _run(self):
        while len(self.tasks) > 0:
            func, args, kwargs = self.tasks.pop(0)
            func(*args, **kwargs)

    def start(self):
        self.thread.start()

    def stop(self):
        pass  # SIGINT


if __name__ == "__main__":
    runner = BackgroundThreadRunner()
    runner.add_task(lambda: print("hello"))
    runner.start()
