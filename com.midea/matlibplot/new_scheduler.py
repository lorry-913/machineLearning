# enccding=utf-8
import sim
import sys


def getScoreMetricTime(thread_id):
    return long(sim.stats.get('thread', thread_id, 'nonidle_elapsed_time'))


def getScoreMetric(thread_id):
    return long(sim.stats.get('thread', thread_id, 'instruction_count'))


class Thread:
    def __init__(self, thread_id):
        self._thread_id = thread_id
        self._ipc = 0  # ignored
        self._core = None
        self._runnable = None
        self._last_scheduled_time = 0
        self._unscheduled = False
        self._score = 0  # Accumulated score
        self._metric_last = 0  # State at start of last interval
        self.getScoreMetric = lambda: getScoreMetric(thread_id)
        sim.thread.set_thread_affinity(self._thread_id, ())

    def updateScore(self):
        metric_now = self.getScoreMetric()
        self._score += metric_now - self._metric_last
        self._metric_last = metric_now

    def setScore(self, score):
        self._score = score
        self._metric_last = self.getScoreMetric()

    def setCore(self, core_id, time=-1):
        self._core = core_id
        if core_id is None:
            self._last_scheduled_time = time
            sim.thread.set_thread_affinity(self._thread_id, ())
        else:
            self._last_scheduled_time = time
            sim.thread.set_thread_affinity(self._thread_id, [c == core_id for c in range(sim.config.ncores)])


class DemoScheduler:
    def setup(self, args):
        self.core_mapping = dict((core, '-') for core in range(sim.config.ncores))
        self.icount_last = [0 for core in range(sim.config.ncores)]
        self.ipc = [0 for core in range(sim.config.ncores)]
        self._last_reschedule = 0  # phase singal
        self._last_ipc = [0 for core in range(sim.config.ncores)]
        self._threshlod = 0.5
        self._threads = {}
        self._last_core = 0
        self._cores = range(sim.config.ncores)  # ignored core mask
        self._core_list = [core for core in range(sim.config.ncores)]
        self._thread_list = [core for core in range(sim.config.ncores)]
        self._t_c_map = [None] * (sim.config.ncores)
        self.getScoreMetric = getScoreMetric
        self._last_time = 0
        """
        PD -   press double precision
        PS -   press single precision
        SD -   scalar double precision
        SS -   scalar single precision
        """
        self.addpd = [0 for core in range(sim.config.ncores)]
        self.addsd = [0 for core in range(sim.config.ncores)]
        self.addss = [0 for core in range(sim.config.ncores)]
        self.addps = [0 for core in range(sim.config.ncores)]

        self.subpd = [0 for core in range(sim.config.ncores)]
        self.subsd = [0 for core in range(sim.config.ncores)]
        self.subss = [0 for core in range(sim.config.ncores)]
        self.subps = [0 for core in range(sim.config.ncores)]

        self.divpd = [0 for core in range(sim.config.ncores)]
        self.divsd = [0 for core in range(sim.config.ncores)]
        self.divss = [0 for core in range(sim.config.ncores)]
        self.divps = [0 for core in range(sim.config.ncores)]

        self.mulpd = [0 for core in range(sim.config.ncores)]
        self.mulsd = [0 for core in range(sim.config.ncores)]
        self.mulss = [0 for core in range(sim.config.ncores)]
        self.mulps = [0 for core in range(sim.config.ncores)]

        self.add = [0 for core in range(sim.config.ncores)]
        self.sub = [0 for core in range(sim.config.ncores)]
        self.mul = [0 for core in range(sim.config.ncores)]
        self.div = [0 for core in range(sim.config.ncores)]

        self.jmp = [0 for core in range(sim.config.ncores)]

        self.l1_i_load = [0 for core in range(sim.config.ncores)]
        self.l1_d_load = [0 for core in range(sim.config.ncores)]
        self.l2_load = [0 for core in range(sim.config.ncores)]
        self.l3_load = [0 for core in range(sim.config.ncores)]

        sim.util.Every(10 * sim.util.Time.US, self.periodic, roi_only=True)

    def hook_thread_migrate(self, threadid, coreid, time):
        self.core_mapping[coreid] = threadid

    def hook_thread_start(self, thread_id, time):
        self._threads[thread_id] = Thread(thread_id)
        self._threads[thread_id]._runnable = True
        # Initial assignment: one thread per core until cores are exhausted
        if self._last_core < len(self._cores):
            self._threads[thread_id].setCore(self._cores[self._last_core], sim.stats.time())
            # self._t_c_map[self._cores[self._last_core]] = thread_id
            self._last_core += 1
        else:
            self._threads[thread_id].setCore(None, sim.stats.time())

    def hook_thread_stall(self, thread_id, reason, time):  # Todo: waiting update t_c_map
        if reason == 'unscheduled':
            # Ignore calls due to the thread being scheduled out
            self._threads[thread_id]._unscheduled = True
        else:
            core = self._threads[thread_id]._core
            self._threads[thread_id].setCore(None, time)
            self._threads[thread_id]._runnable = False
            # Schedule a new thread (runnable, but not running) on this free core
            threads = [thread for thread in self._threads.values() if thread._runnable and thread._core is None]
            if threads:
                # Order by score
                threads.sort(key=lambda thread: thread.score)
                threads[0].setCore(core, time)
                print('=> [stall]: thread_id {} is mapped to core_id {}'.format(threads[0]._thread_id, core))

    def hook_thread_exit(self, thread_id, time):
        self.hook_thread_stall(thread_id, 'exit', time)

    def hook_thread_resume(self, thread_id, woken_by, time):  # Todo: waiting update t_c_map
        if self._threads[thread_id]._unscheduled:
            # Ignore calls due to the thread being scheduled back in
            self._threads[thread_id]._unscheduled = False
        else:
            self._threads[thread_id].setScore(min([thread._score for thread in self._threads.values()]))
            self._threads[thread_id]._runnable = True
            # If there is a free core, move us there now
            used_cores = set([thread._core for thread in self._threads.values() if thread._core is not None])
            free_cores = set(self._cores) - used_cores
            if len(free_cores):
                self._threads[thread_id].setCore(list(free_cores)[0], time)
                print('=> [resume]: thread_id {} is mapped to core_id {}'.format(thread_id, list(free_cores)[0]))

    def periodic(self, time, time_delta):
        print("zhouqixingde1")
        #    print('------------------- time_delta is {}'.format(time_delta))
        if time_delta:
            for core in range(sim.config.ncores):
                icount = sim.stats.get('performance_model', core, 'instruction_count')
                print("-------------icount:" + str(icount))
                icount_diff = float(icount - self.icount_last[core])
                cycles = float(time_delta * sim.dvfs.get_frequency(core) / 1e9)
                print(cycles)
                self.icount_last[core] = icount
                self.ipc[core] = float(icount_diff / cycles)
                print("------------ipc[core]:" + str(float(icount_diff / cycles)))
                self.add[core] = sim.stats.get('instruction_tracer', core, 'ADD')
                self.sub[core] = sim.stats.get('instruction_tracer', core, 'SUB')
                self.mul[core] = sim.stats.get('instruction_tracer', core, 'MUL')
                self.div[core] = sim.stats.get('instruction_tracer', core, 'DIV')
                self.jmp[core] = sim.stats.get('instruction_tracer', core, 'JMP')

                self.l1_i_load[core] = sim.stats.get('L1-I', core, 'loads')
                print("------------l1_i_load[core]:" + str(sim.stats.get('L1-I', core, 'loads')))
                self.l1_d_load[core] = sim.stats.get('L1-D', core, 'loads')
                self.l2_load[core] = sim.stats.get('L2', core, 'loads')
                self.l3_load[core] = sim.stats.get('L3', core, 'loads')
            # self.save_metric()
            core_list = [thread._core for thread in self._threads.values()]
            thread_list = [thread._thread_id for thread in self._threads.values()]

            print(' ---> [core_list]: {}'.format(core_list))
            #      print(' ---> [thread_list]: {}'.format(thread_list))

            for thread_id, core_id in zip(thread_list, core_list):  # thread id which mapped to core
                if core_id is not None:
                    self._t_c_map[core_id] = thread_id
            #      print(' ---> [_t_c_map]: {}'.format(self._t_c_map))
            self._last_reschedule = any(map(lambda x: float(x) > self._threshlod,
                                            map(lambda c: float(c[1]) / float(c[0] + 1e-5), zip(self.ipc, list(
                                                map(lambda c: abs(float(c[0]) - float(c[1])),
                                                    zip(self.ipc, self._last_ipc)))))))

            # print('--->[debug]: phase switch is {}'.format(map(lambda x: float(x) > self._threshlod,
            map(lambda c: float(c[1]) / float(c[0] + 1e-5),
                zip(self.ipc, list(map(lambda c: abs(float(c[0]) - float(c[1])), zip(self.ipc, self._last_ipc)))))

            # print('--->[debug]: ipc delta is {}'.format(
            #  map(lambda c: float(c[1]) / float(c[0] + 1e-5), zip(self.ipc, list(
            #    map(lambda c: abs(float(c[0]) - float(c[1])), zip(self.ipc, self._last_ipc)))))))

            # print('--->[debug]: current ipc is {}'.format([float(self.ipc[core]) for core in range(sim.config.ncores)]))

            # print('--->[debug]: last ipc is {}'.format([float(self._last_ipc[core]) for core in range(sim.config.ncores)]))

            # self._last_reschedul = sum(map(lambda c: float(c[1]) / float(c[0]),
            #   zip(self.ipc, list(map(lambda c: abs(float(c[0]) - float(c[1])),
            #    zip(self.ipc, self._last_ipc)))))) < self._threshlod
            self._last_ipc = [float(self.ipc[core]) for core in range(sim.config.ncores)]

        if time - self._last_time >= 60e9:
            self._last_time = time
            self._last_reschedule = True
            self.reschedule()
            self._last_reschedule = False
            # self.save_metric()

    def save_metric(self):
        savedOut = sys.stdout
        sys.stdout = open('feature_data.txt', 'a+')

        print('{}-{}-{}-{}-{}-{}-{}-{}-{}-{}'.format([self.add[core] for core in range(sim.config.ncores)]
                                                     , [self.sub[core] for core in range(sim.config.ncores)]
                                                     , [self.mul[core] for core in range(sim.config.ncores)]
                                                     , [self.div[core] for core in range(sim.config.ncores)]
                                                     , [self.jmp[core] for core in range(sim.config.ncores)]
                                                     , [self.l1_i_load[core] for core in range(sim.config.ncores)]
                                                     , [self.l1_d_load[core] for core in range(sim.config.ncores)]
                                                     , [self.l2_load[core] for core in range(sim.config.ncores)]
                                                     , [self.l3_load[core] for core in range(sim.config.ncores)]
                                                     , [float(self.ipc[core]) for core in range(sim.config.ncores)]))

        sys.stdout = savedOut

    def print_info(self):

        print('[time]: {}'.format(sim.stats.time() / 1e9))
        print('[mapping] {}'.format([str(self.core_mapping[core]) for core in range(sim.config.ncores)]))
        print('[ADD]: {}'.format([self.add[core] for core in range(sim.config.ncores)]))
        print('[SUB]: {}'.format([self.sub[core] for core in range(sim.config.ncores)]))
        print('[MUL]: {}'.format([self.mul[core] for core in range(sim.config.ncores)]))
        print('[DIV]: {}'.format([self.div[core] for core in range(sim.config.ncores)]))
        print('[JMP]: {}'.format([self.jmp[core] for core in range(sim.config.ncores)]))
        print('[L1-I]: {}'.format([self.l1_i_load[core] for core in range(sim.config.ncores)]))
        print('[L1-D]: {}'.format([self.l1_d_load[core] for core in range(sim.config.ncores)]))
        print('[L2]: {}'.format([self.l2_load[core] for core in range(sim.config.ncores)]))
        print('[L3]: {}'.format([self.l3_load[core] for core in range(sim.config.ncores)]))
        print('[ipc]: {}'.format([float(self.ipc[core]) for core in range(sim.config.ncores)]))

    def hook_roi_end(self):
        print('-------------------')
        print('[DEMO] Total runtime = {} us'.format(sim.stats.time() / 1e9))
        print('-------------------')

    def reschedule(self):
        if self._last_reschedule:
            threads = [(thread, sim.stats.get('thread', thread, 'instruction_count'))
                       for thread in range(sim.thread.get_nthreads())]
            #     print('--->[debug]: thread numbers is :{}'.format(sim.thread.get_nthreads()))
            #     print('--->[debug]: thread instruction_count is : {}'.format(threads))
            threads.sort(key=lambda (thread, icount): icount, reverse=False)
            print('--->[debug]: after sored, thread instruction_count is : {}'.format(threads))
            print('=> [reschedule before]: t_c_map is {}'.format(self._t_c_map))
            mapping_list = [1, 3, 2, 0]

            for core_id, mapping_id in enumerate(mapping_list):
                thread_id = self._t_c_map[mapping_id]
                self._threads[thread_id].setCore(core_id)
            for i in self._threads:
                print('thread_id {} => core_id {}'.format(self._threads[i]._thread_id, self._threads[i]._core))
                self._t_c_map[self._threads[i]._core] = self._threads[i]._thread_id

            print('=> [reschedule after]: t_c_map is {}'.format(self._t_c_map))

            '''
            print('[DEMO] Reschedule: ')
            for i, (thread, _) in enumerate(threads):
              affinity = [ core == i for core in range(sim.config.ncores) ]
              sim.thread.set_thread_affinity(thread, affinity)
              print('thread_{} => core_{}'.format(thread, i))
            '''


sim.util.register(DemoScheduler())