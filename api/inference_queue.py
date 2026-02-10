import threading
import uuid
from queue import Queue
from typing import Callable, Any, Dict


class Job:
    def __init__(self, function: Callable[[], Any], job_type: str):
        self.id = str(uuid.uuid4())
        self.function = function
        self.type = job_type
        self.status = "queued"
        self.result: str | None = None
        self.error: str | None = None


class JobQueue:
    def __init__(self):
        self.queue: Queue[Job] = Queue()
        self.jobs: Dict[str, Job] = {}

        self.worker = threading.Thread(
            target=self._worker_loop,
            daemon=True,
        )
        self.worker.start()

    def submit(self, fn: Callable[[], Any], job_type: str) -> str:
        job = Job(fn, job_type)
        self.jobs[job.id] = job
        self.queue.put(job)
        return job.id

    def get(self, job_id: str) -> Job:
        return self.jobs.get(job_id)

    def _worker_loop(self):
        while True:
            job = self.queue.get()
            job.status = "running"
            try:
                job.result = job.function()
                job.status = "done"
            except Exception as e:
                job.error = str(e)
                job.status = "error"
            finally:
                self.queue.task_done()