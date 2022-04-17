import threading
import time

class Ticket(object):
    def __init__(self, num):
        self.num = num
    
def sell_ticket(ticket):
    print(threading.current_thread().name, "address ticket:{}".format(id(ticket)))
    while True:
        if ticket.num > 10:
            time.sleep(0.1)
            ticket.num -= 1
        else:
            return
        print(threading.current_thread().name,f" ticket num:{ticket.num}")

lock = threading.Lock()
def sell_ticket_safe(ticket):
    print(threading.current_thread().name, "address ticket:{}".format(id(ticket)))
    while True:
        with lock:
            if ticket.num > 10:
                time.sleep(0.1)
                ticket.num -= 1
            else:
                return
        print(threading.current_thread().name,f" ticket num:{ticket.num}")

def start_sell_ticket(ticket, function):
    threads = [threading.Thread(target=function, args=(ticket,), name=f"{function.__name__}_{i}") for i in range(3)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == '__main__':
    ticket = Ticket(30)
    print("main thread address ticket:{}".format(id(ticket)))
    start_sell_ticket(ticket, sell_ticket)
    ticket_ = Ticket(30)
    start_sell_ticket(ticket_, sell_ticket_safe)
    
    print("main thread over!")