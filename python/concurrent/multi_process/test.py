from multiprocessing import Manager, current_process
import multiprocessing as mp
import random


class ExampleClass:
    def __init__(self, stringVar):
        # these variables aren't saved across processes?
        self.stringVar = stringVar
        self.count = 0


class ProcessContainer(object):
    processes = []

    def __init__(self, *args, **kwargs):
        manager = Manager()
        self.dict = manager.dict()

    def f1(self, dict):
        # generate a random index to add the class to
        index = str(random.randint(0, 100))

        # create a new class at that index
        dict[index] = ExampleClass(str(random.randint(100, 200)))

        # this is the problem, it doesn't share the updated variables in the dictionary between the processes <----------------------
        # attempt to change the created variables
        ec = dict[index]
        ec.count += 1
        ec.stringVar = "yeAH"
        dict[index] = ec # show new reference
        # print what's inside
        print(current_process().name ,index, ec.count)


    def f(self, dict):
        # generate a random index to add the class to
        index = str(random.randint(0, 100))

        # create a new class at that index
        dict[index] = ExampleClass(str(random.randint(100, 200)))
        dict[index].count += 1
        dict[index].stringVar = "yeAH"

        # print what's inside
        print(current_process().name ,index, dict[index].count)

    def Run(self):
        # create the processes
        # self.processes = [mp.Process(target=self.f, args=(self.dict,), name=f"process_{i}") for i in range(3)]
        for str in range(3):
            p = mp.Process(target=self.f, args=(self.dict,))
            self.processes.append(p)
        # start the processes
        [proc.start() for proc in self.processes]

        # wait for the processes to finish
        [proc.join() for proc in self.processes]
        print(self.dict)


if __name__ == '__main__':
    test = ProcessContainer()
    test.Run()
