"""
System's Operational Scheduler Intentionally Ambitious - SOSIA 

"""
from simso.core import Scheduler

class SOSIA(Scheduler):
    def init(self):
        self.ready_list = []

    def on_activate(self, job):
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            # job with the highest priority
            job = min(self.ready_list, key=lambda x: (x.absolute_deadline - x.wcet + 5*x.period/10))
        else:
            job = None

        return (job, cpu)

