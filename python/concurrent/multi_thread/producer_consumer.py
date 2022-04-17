from bs4 import BeautifulSoup
from requests import request
import base
import queue
import time
import random
 
def producer_craw(url_queue:queue.Queue, html_queue:queue.Queue):
    while True:
        if url_queue.qsize() == 0:
            print(base.threading.current_thread().name," quit")
            return
        url = url_queue.get()
        result = base.craw(url=url)
        html_queue.put(result)
        print(base.threading.current_thread().name, f" url:{url}","url_queue.size=",url_queue.qsize())
        time.sleep(random.randint(1,2))
 
def consumer_parse(html_queue:queue.Queue, fout):
    try_count = 0
    while True:
        if try_count >=3:
            print(base.threading.current_thread().name," quit")
            return          
        try:
            html = html_queue.get(timeout=2)
        except Exception as e:
            try_count +=1
        else:            
            soup = BeautifulSoup(html.text, "html.parser")
            links = soup.find_all("a", class_="post-item-title")
            result = [(link["href"], link.get_text()) for link in links]
            # for link in links:
            #     print("producer_craw links:{}".format(link["href"], link.get_text()))
            for item in result:
                fout.write(str.encode(str(item)+"\n"))
            
            print(base.threading.current_thread().name, f" result.size",len(result),"html_queue.size=", html_queue.qsize())
            time.sleep(random.randint(1,2))    
                  
        
 
if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    [url_queue.put(url) for url in base.urls]
    print("url_queue.qsize={}".format(url_queue.qsize()))
    thread_craw=[base.threading.Thread(target=producer_craw, args=(url_queue, html_queue), name=f"craw_{i}") for i in range(3)]
    [thread.start() for thread in thread_craw]
    
    fout = open("1.data.txt", "wb+")
    thread_parse=[base.threading.Thread(target=consumer_parse, args=(html_queue, fout,), name=f"parse_{i}") for i in range(2)]
    [thread.start() for thread in thread_parse]
    
    
    [thread.join() for thread in thread_craw]
    [thread.join() for thread in thread_parse]
    print("main thread is exit!")