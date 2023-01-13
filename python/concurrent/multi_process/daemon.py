from logging import raiseExceptions
import multiprocessing
import queue
import traceback
import os
from multiprocessing import Manager, Lock

from time import sleep

class Process(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._parent_conn, self._child_conn = multiprocessing.Pipe()
        self._exception = None
    
    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._child_conn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._child_conn.send((e, tb))
    
    @property
    def exception(self):
        if self._parent_conn.poll():
            self._exception = self._parent_conn.recv()
        return self._exception
    
class Task(object):
    def __init__(self, user):
        self.user = user
    # def do_task(self, param):
    #     print(f'child Pid{os.getpid()} user:{self.user}')
    #     param.put(dict(user=self.user))
    #     if self.user % 2 == 0:
    #         2 % 0
    def do_task(self, param):
        param[os.getpid()] = self.user
        if self.user % 2 == 0:
            2 % 0
    
def main():
    try:
        # task_1 = Task(2)
        # task_2 = Task(5)

        # task_param = multiprocessing.Queue()
        # task_1_process = Process(
        #     target=task_1.do_task,
        #     kwargs=dict(queue=task_param)
        # )
        
        # task_2_process = Process(
        #     target=task_2.do_task,
        #     kwargs=dict(queue=task_param)
        # )
        # task_process_list = [task_1_process, task_2_process]

        task_param = Manager().dict()
        task_param['test'] = {}
        task_process_list = [Process(target=Task(i).do_task, kwargs=dict(param=task_param)) for i in range(2)]
        [task.start() for task in task_process_list]
        print(f'Parent Pid:{os.getpid()}')
        index = 6
        while True:
            for task in list(task_process_list):
                sleep(1)
                if not task.is_alive():
                    print(f'process nums:{len(task_process_list)},task_dict:{task_param}')
                    task.join()
                    task_ = Task(index)
                    index += 1
                    task_process = Process(
                        target=task_.do_task,
                        kwargs=dict(param=task_param)
                    )
                    task_process.start()
                    task_process_list.remove(task)
                    task_process_list.append(task_process)
                if task.exception:
                    error, _traceback = task.exception
                    task.terminate()
                    print(f'error:{error}, traceback{_traceback}')
        
        [task.join() for task in task_process_list]

    except Exception as e:
        print(f'traceback:{traceback.format_exc()}')

if __name__ == '__main__':
    main()