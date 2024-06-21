import time
from datetime import datetime
from multiprocessing import Process

from schedule import Scheduler


class MPScheduler(Scheduler):
    def __init__(self, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        super(MPScheduler, self).__init__(*args, **kwargs)
        # Among other things, this object inherits self.jobs (a list of jobs)
        self.args = args
        self.kwargs = kwargs
        self.processes = list()

    def _mp_run_job(self, job_func):
        """Spawn another process to run the job; multiprocessing avoids GIL issues"""
        job_process = Process(target=job_func, args=self.args, kwargs=self.kwargs)
        job_process.daemon = True
        job_process.start()
        self.processes.append(job_process)

    def run_pending(self):
        """Run any jobs which are ready"""
        runnable_jobs = (job_obj for job_obj in self.jobs if job_obj.should_run)
        for job_obj in sorted(runnable_jobs):
            job_obj.last_run = datetime.now()  # Housekeeping
            self._mp_run_job(job_obj.job_func)
            job_obj._schedule_next_run()  # Schedule the next execution datetime

        self._retire_finished_processes()

    def _retire_finished_processes(self):
        """Walk the list of processes and retire finished processes"""
        retirement_list = list()  # List of process objects to remove
        for idx, process in enumerate(self.processes):
            if process.is_alive():
                # wait a short time for process to finish
                process.join(0.01)
            else:
                retirement_list.append(idx)

        ## Retire finished processes
        for process_idx in sorted(retirement_list, reverse=True):
            self.processes.pop(process_idx)


def job(id, hungry=True):
    print('{} running {} and hungry={}'.format(datetime.now(), id, hungry))
    time.sleep(10)  # This job runs without blocking execution of other jobs


if __name__ == '__main__':
    # Build a schedule of overlapping jobs...
    mp_sched = MPScheduler()
    mp_sched.every(1).seconds.do(job, id=1, hungry=False)
    mp_sched.every(2).seconds.do(job, id=2)
    mp_sched.every(3).seconds.do(job, id=3)
    mp_sched.every(4).seconds.do(job, id=4)
    mp_sched.every(5).seconds.do(job, id=5)

    while True:
        mp_sched.run_pending()
        time.sleep(1)
