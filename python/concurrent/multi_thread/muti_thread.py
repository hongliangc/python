#-*- coding: utf-8 -*-
'''
多进程Process(multiprocessing) 
优点：可以利用多核cpu并行运算
缺点：占用资源多，可以用数目比线程少
适用于：CPU密集型计算，比如压缩，解压缩

多线程Thread(threading)
优点：相比进程轻量，占用资源少
缺点：
    相比进程：多线程只能并发执行，不能利用多cpu（GIL）
    相比协程：启动数目有限制，占用资源多，线程切换有开销
适用于：IO密集型计算，同时运行的数目要求不多， I/O(read,write,send,recv,etc.)
1.多线程用于IO密集型计算时，IO期间线程会释放GIL,实现CPU和IO的并行，因此多线程用于IO密集型计算依然可以大幅提升计算
2.多线程用于CPU密集型计算时，一次只能运行一个线程，只会更加拖慢速递

多协程Coroutine(asyncio)
优点：内存开销最新，启动协程数量最多
缺点：支持的库有限制(aiohttp vs request)，代码实现复杂
适用于：IO密集型计算，需要超多任务的运行，但实现需要协程库的执行

GIL(Global Interpreter Lock)全局解释器锁
用于线程同步机制，任何时刻只能运行一个线程
1.when a thread is running,it holds the gGIL 
线程运行的时候持有GIL锁
2.GIL released on I/O(read,write,send,recv,etc.)
执行线程遇到IO操作的时会释放GIL锁，其它线程获取GIL锁运行
'''
import threading
import base
import time


def signal_craw(urls):
    for url in urls:
        result = base.craw(url)
        #print(result))
        
def multithread_craw(urls):
    threads = []
    for url in urls:
        threads.append(base.ThreadEx(target=base.craw, args=(url,)))
        #threads.append(threading.Thread(target=base.craw, args=(url,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
        #print(thread.result)
        
if __name__ == '__main__':
    
    t1 = time.time()
    print("signal_craw start")
    signal_craw(base.urls)
    t2 = time.time()
    print(f"************** signal_craw end cost time:{t2-t1}")

    print("multithread_craw start")
    multithread_craw(base.urls)
    t3 = time.time()
    print(f"************** multithread_craw end cost time:{t3-t2}")
    
    print("************** multithread_craw faster %.2f tiems than signal_craw" % ((t2-t1)/(t3-t2)))