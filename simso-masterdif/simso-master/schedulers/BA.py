"""
My own creation! It needs to BECOME ALIVE!!
"""
from simso.core import Scheduler, Timer

class BA(Scheduler):
    def init(self):
        self.ready_list = [] #Lista de processos na Fila de Espera
        self.guard_list = [] #Lista de processos que já executaram
        self.ready_len = 0 #Quantidade de processos na Fila
        self.guard_len = 0 #Quantidade de processos na Fila dos já executados
        self.percent_process = 0 #Razao guard_len /(ready_len + guard_len)
        self.running_job = None
        self.quantum = 1 # ms
        self.percent_limit = 0.2
        self.total_deadline = 0
        self.first_process = None
        self.timer = Timer(self.sim, BA.reschedule,
                          (self, self.processors[0]), self.quantum,
                          cpu=self.processors[0])
        self.timer.start()

    def reschedule(self, cpu):
        if(self.ready_len != 0 or self.guard_len != 0):
            self.percent_process = self.guard_len/(self.ready_len + self.guard_len)

        if self.ready_len > 0:
            if self.percent_process > self.percent_limit:
                self.ready_list.extend(self.guard_list)
                self.guard_list.clear()

                self.ready_len += self.guard_len
                self.guard_len = 0

            self.new_quantum()
            cpu.resched()
        elif self.guard_len > 0:
            self.ready_list.extend(self.guard_list)
            self.guard_list.clear()

            self.ready_len += self.guard_len
            self.guard_len = 0

            self.new_quantum()
            cpu.resched()
        else:
            self.new_quantum()

    def on_activate(self, job):
        self.ready_list.append(job)
        self.total_deadline += job.absolute_deadline
        self.ready_len += 1;

        job.cpu.resched()

    def on_terminated(self, job):
        self.total_deadline -= job.absolute_deadline
        self.running_job = None

        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_len > 0:
            job = min(self.ready_list, key=lambda x: x.absolute_deadline)
            self.ready_list.remove(job)
            self.ready_len -= 1

            if self.running_job is not None:
                self.guard_len += 1
                self.guard_list.append(self.running_job)

            self.running_job = job

        else:
            job = self.running_job

        return (job, cpu)

    def new_quantum(self):
        self.timer = Timer(self.sim, BA.reschedule,
                          (self, self.processors[0]), self.quantum,
                          cpu=self.processors[0])
        self.timer.start()
