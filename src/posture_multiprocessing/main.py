from multiprocessing import Process, freeze_support

from posture1 import process1
from posture2 import process2
from posture3 import process3

if __name__ == "__main__":
    freeze_support()
    p1 = Process(target=process1)
    p2 = Process(target=process2)
    p3 = Process(target=process3)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()