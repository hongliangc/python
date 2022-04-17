import requests
import threading

urls = [ f"https://www.cnblogs.com/#p{page}" for page in range(0, 50)]

def craw(url):
    r = requests.get(url)
    return r

craw(urls[0])

'''
支持返回的线程
'''
class ThreadEx(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)
    
'''

import Queue             # Python 2.x
#from queue import Queue # Python 3.x

from threading import Thread

def foo(bar):
    print 'hello {0}'.format(bar)
    return 'foo'

que = Queue.Queue()      # Python 2.x
#que = Queue()           # Python 3.x

t = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
t.start()
t.join()
result = que.get()
print result
'''        