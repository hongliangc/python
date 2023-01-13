import time
import multiprocessing as mp


def process_f(key, shared_dict):
        values = [i for i in range(64 * 1024 * 1024)]
        print("Writing {}...".format(key))
        a = time.time()
        shared_dict[key] = values
        b = time.time()
        print("released {} in {}ms".format(key, (b-a)*1000))


def main():
    process_manager = mp.Manager()
    n = 5
    keys = [i for i in range(n)]
    shared_dict = process_manager.dict({i: i * i for i in keys})

    pool = mp.Pool(processes=n)

    for i in range(n):
        pool.apply_async(process_f, (keys[i], shared_dict))
    time.sleep(20)


if __name__ == '__main__':
    main()