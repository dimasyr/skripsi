import threading, time
import matplotlib.pyplot as plt
from random import randrange

class coba:
    def tambahx(self, x):
        total = 0
        for i in range(5):
            total += int(x)
            time.sleep(1)
            print(total)

    def tambahy(self, y):
        total = 0
        for i in range(5):
            total += int(y)
            time.sleep(1)
            print(total)

if __name__  == '__main__':
    data = []
    for i in range(50):
        data.append(randrange(100))
    print(plt.style.available)
    plt.style.use('_classic_test')
    plt.plot(data, 'r')
    plt.xlabel('time (ms)')
    plt.ylabel('CPU (%)')
    plt.title('CPU Usage of Mining')
    plt.grid(True)
    plt.show()