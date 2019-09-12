import psutil
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

class RecordCPU:
    def __init__(self):
        self.cpu_usage_publish = []
        self.cpu_usage_search = []
        self.is_mining = False
        self.record_cpu = False
        self.search_results = []
        self.mean_publish = []
        self.mean_search = []
        self.fontP = FontProperties()

        self.fontP.set_size('small')

    def recordCpuUsage(self, opt = 'publish'):
        while self.is_mining:
            global temp
            temp = []

            while self.record_cpu:
                temp.append(psutil.cpu_percent(0.1))

            if len(temp) != 0:
                if opt == 'publish':
                    self.cpu_usage_publish.append(temp)
                    print('selesai append ke list')
                elif opt == 'search':
                    self.cpu_usage_search.append(temp)

        if self.is_mining == False and opt == 'publish':
            self.mean_publish.append(self.countMean(self.cpu_usage_publish[-1]))

        if self.is_mining == False and opt == 'search':
            self.mean_search.append(self.countMean(self.cpu_usage_search[-1]))

        print('mining doneeeee')

    def countMean(self, list):
        jumlah = sum(list)
        total = len(list)

        return float(jumlah/total)

    def printCpuUsage(self, opt = 'publish', savefig = False):
        fig = plt.figure()

        if opt == 'publish':
            if len(self.cpu_usage_publish) != 0:
                for i in range(len(self.cpu_usage_publish)):
                    global temp
                    temp = []
                    for x in range(len(self.cpu_usage_publish[i])):
                        temp.append(self.mean_publish[i])

                    plt.style.use('classic')
                    plt.plot(self.cpu_usage_publish[i], color ='r', label = 'CPU usage')
                    plt.plot(temp, color = 'g', label = 'nilai rata-rata')
                    temp = []
                    plt.xlabel('time (ms)')
                    plt.ylabel('CPU (%)')
                    plt.title('CPU Usage of Mining')
                    plt.legend(loc = 3, prop = self.fontP)
                    plt.grid(True)
                    if savefig:
                        namefig = 'CPU usage of mining ' + str(i)
                        plt.savefig(namefig)
                        fig.clear()
                    else:
                        plt.show()
            else:
                print('data belum ada')

        #terakhir ngerjakno save figure
        elif opt == 'search':
            if len(self.cpu_usage_search) != 0:
                temp = []
                for i in range(len(self.cpu_usage_search)):
                    for x in range(len(self.cpu_usage_search[i])):
                        temp.append(self.mean_search[i])

                    plt.style.use('classic')
                    plt.plot(self.cpu_usage_search[i], color='r', label='CPU usage')
                    plt.plot(temp, color='g', label='nilai rata-rata')
                    temp = []
                    plt.xlabel('time (ms)')
                    plt.ylabel('CPU (%)')
                    plt.title('CPU Usage of Search')
                    plt.legend(loc = 3, prop = self.fontP)
                    plt.grid(True)

                    if savefig:
                        namefig = 'CPU usage of search' + str(i)
                        plt.savefig(namefig)
                    else:
                        plt.show()
            else:
                print('data belum ada')
        else:
            print('data tidak ada')


    def lenCPU(self, opt = 'publish'):
        if opt == 'publish':
            print(len(self.cpu_usage_publish))
        elif opt == 'search':
            print(len(self.cpu_usage_search))
        else:
            print('data tidak ada')