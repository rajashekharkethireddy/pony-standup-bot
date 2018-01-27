# coding=utf-8
import time
import collections


class TasksQueue(object):
    """World tick queue."""
    def __init__(self, bot, interval):
        self._bot = bot
        self._interval = interval
        self._queue = collections.deque()
        self._last_run_at = time.time()

    def _is_time_to_run(self):
        if time.time() - self._last_run_at > self._interval:
            return True

        return False

    def append(self, task):
        self._queue.append(task)

    def process(self):
        if not self._is_time_to_run():
            return

        visible_tasks = len(self._queue)

        for x in range(visible_tasks):
            task = self._queue.popleft()
            try:
                task.execute(bot=self._bot)
            except Exception as e:
                self._bot.log.error(
                    'Error processing task {}\n{}'.format(task, e))

                if self._bot.debug:
                    raise

        self._last_run_at = time.time()