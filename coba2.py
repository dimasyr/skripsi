import threading, time
import matplotlib.pyplot as plt
from random import randrange
from matplotlib.font_manager import FontProperties

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

    def mean(self, list):
        jumlah = sum(list)
        total = len(list)
        return float(jumlah/total)

if __name__  == '__main__':
    # c = coba()
    # data = [5]
    # print(data[-1])

    fig = plt.figure()

    fontP = FontProperties()
    fontP.set_size('small')

    for x in range(3):
        data = []
        for i in range(50):
            data.append(randrange(100))
        print(plt.style.available)
        plt.style.use('classic')
        plt.plot(data, 'r', label = 'asd')
        plt.xlabel('time (ms)')
        plt.ylabel('CPU (%)')
        plt.title('CPU Usage of Mining')
        plt.legend(loc = 3, prop = fontP)
        # plt.tight_layout()
        plt.grid(True)
        namefig = 'CPU usage of mining ' + str(x)
        # plt.savefig(namefig)
        # fig.clear()
        plt.show()