import psutil
import matplotlib.pyplot as plt

class RecordCPU:
    def __init__(self):
        self.cpu_usage_publish = []
        self.cpu_usage_search = []
        self.is_mining = False
        self.record_cpu = False
        self.search_results = []

    def recordCpuUsage(self, opt):
        while self.is_mining:
            global temp
            temp = []

            while self.record_cpu:
                temp.append(psutil.cpu_percent(0.1))

            if len(temp) != 0:
                if opt == 'publish':
                    self.cpu_usage_publish.append(temp)
                elif opt == 'search':
                    self.cpu_usage_search.append(temp)

    def printCpuUsage(self, opt = 'publish'):
        if opt == 'publish':
            if len(self.cpu_usage_publish) != 0:
                for i in range(len(self.cpu_usage_publish)):
                    plt.plot(self.cpu_usage_publish[i], 'r--')
                    plt.show()
            else:
                print('data belum ada')

        elif opt == 'search':
            if len(self.cpu_usage_search) != 0:
                for i in range(len(self.cpu_usage_search)):
                    plt.plot(self.cpu_usage_search[i], 'r--')
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