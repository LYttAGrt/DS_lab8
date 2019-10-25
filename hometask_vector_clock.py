# src: https://towardsdatascience.com/understanding-lamport-timestamps-with-pythons-multiprocessing-library-12a6427881c6
# push this to the https://github.com/LYttAGrt/DS_lab8
# print results & add them to the README

from multiprocessing import Process, Pipe
# from os import getpid
from datetime import datetime

from time import sleep


def local_time(counter):
    return '(LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    for counter_id in range(len(counter)):
        counter[counter_id] = max(recv_time_stamp[counter_id], counter[counter_id])
    return counter


def event(pid, counter):
    counter[pid] += 1
    print('Proc_{}:'.format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid) + local_time(counter))
    return counter


def process_one(pipe12):
    pid = 0
    counter = [0, 0, 0]

    counter = send_message(pipe12, pid, counter)

    counter = send_message(pipe12, pid, counter)

    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    sleep(2)

    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    print('Process', pid, '->', counter)


def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]

    counter = event(pid, counter)
    counter = recv_message(pipe21, pid, counter)

    counter = event(pid, counter)
    counter = recv_message(pipe21, pid, counter)

    counter = send_message(pipe21, pid, counter)

    counter = event(pid, counter)
    counter = recv_message(pipe23, pid, counter)
    sleep(1)

    counter = send_message(pipe21, pid, counter)

    counter = send_message(pipe23, pid, counter)

    counter = send_message(pipe23, pid, counter)
    print('Process', pid, '->', counter)


def process_three(pipe32):
    pid = 2
    counter = [0, 0, 0]

    counter = send_message(pipe32, pid, counter)

    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)
    sleep(1)

    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)
    print('Process', pid, '->', counter)


"""
    I'll use event() function only when recv() called, since only send() increases events' counter
"""
if __name__ == '__main__':
    pipe12, pipe21 = Pipe()
    pipe23, pipe32 = Pipe()

    process1 = Process(target=process_one, args=(pipe12,))
    process2 = Process(target=process_two, args=(pipe21, pipe23))
    process3 = Process(target=process_three, args=(pipe32,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
