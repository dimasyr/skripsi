import psutil
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from joblib import load, dump

class RecordCPU:
    def __init__(self):
        self.cpu_usage_publish = []
        self.cpu_usage_search = []
		
        self.is_mining = False
        self.record_cpu = False
        self.search_results = []
        self.mean_publish = []
        self.mean_search = []
        self.list_miner = []
        self.publish_time = []
        self.search_time = []
        self.fontP = FontProperties()
        self.fontP.set_size('small')
        self.final_mean_publish = []
        self.final_mean_search = []
        self.final_publish_time = []
        self.final_search_time = []
		

    # merekam data penggunaan CPU
    def recordCpuUsage(self, opt = 'publish'):
        while self.is_mining:
            global temp
            temp = []

            while self.record_cpu:
                temp.append(round(psutil.cpu_percent(0.1),2))

            if len(temp) != 0:
                if opt == 'publish':
                    self.cpu_usage_publish.append(temp)
                    # print('selesai append ke list')
                elif opt == 'search':
                    self.cpu_usage_search.append(temp)

        if self.is_mining == False and opt == 'publish':
            self.mean_publish.append(self.countMean(self.cpu_usage_publish[-1]))
            print('Proses mining selesai.\n')

        if self.is_mining == False and opt == 'search':
            self.mean_search.append(self.countMean(self.cpu_usage_search[-1]))
            print('Proses searching selesai.\n')



    # menghitung rata2 penggunaan CPU
    def countMean(self, list):
        jumlah = sum(list)
        total = len(list)

        return round(float(jumlah/total),2)

    def getFinalMean(self):
        self.final_mean_publish = self.countMean(self.mean_publish)
        self.final_mean_search = self.countMean(self.mean_search)
        self.final_publish_time = self.countMean(self.publish_time)
        self.final_search_time = self.countMean(self.search_time)

    # merekam penggunaan CPU (menyimpan hasilnya = opsional)
    def printCpuUsage(self, opt = 'publish', savefig = False):
        if opt == 'publish':
            if len(self.cpu_usage_publish) != 0:
                fig = plt.figure()
                for i in range(len(self.cpu_usage_publish)):
                    global temp
                    temp = []

                    for x in range(len(self.cpu_usage_publish[i])):
                        temp.append(self.mean_publish[i])

                    plt.annotate(str(round(self.mean_publish[i],2)), xy=(1, 1), xytext=(len(self.cpu_usage_publish[i]), self.mean_publish[i]-1))
                    plt.plot(self.cpu_usage_publish[i], color ='r', label = 'CPU usage')
                    plt.plot(temp, color = 'g', label = 'nilai rata-rata')

                    plt.xlabel('time (ms)')
                    plt.ylabel('CPU (%)')
                    plt.title('CPU Usage of Mining')
                    plt.legend(loc = 3, prop = self.fontP)
                    plt.grid(True)

                    if savefig:
                        namefig = 'cpu_usage_publish\CPU usage of mining ' + str(i)
                        plt.savefig(namefig)
                        fig.clear()
                    else:
                        plt.show()
            else:
                print('data publish belum ada')

        elif opt == 'search':
            if len(self.cpu_usage_search) != 0:
                fig = plt.figure()
                for i in range(len(self.cpu_usage_search)):

                    temp = []

                    for x in range(len(self.cpu_usage_search[i])):
                        temp.append(self.mean_search[i])

                    plt.annotate(str(round(self.mean_search[i], 2)), xy=(1, 1),
                                 xytext=(len(self.cpu_usage_search[i]), self.mean_search[i] - 1))
                    plt.plot(self.cpu_usage_search[i], color='r', label='CPU usage')
                    plt.plot(temp, color='g', label='nilai rata-rata')

                    plt.xlabel('time (ms)')
                    plt.ylabel('CPU (%)')
                    plt.title('CPU Usage of Searching')
                    plt.legend(loc=3, prop=self.fontP)
                    plt.grid(True)

                    if savefig:
                        namefig = 'cpu_usage_search\CPU usage of search ' + str(i)
                        plt.savefig(namefig)
                        fig.clear()
                    else:
                        plt.show()
            else:
                print('data search belum ada')

        else:
            print('data tidak ada')

    # melihat panjang data list penggunaan cpu
    def lenCPU(self, opt = 'publish'):
        if opt == 'publish':
            print(len(self.cpu_usage_publish))
        elif opt == 'search':
            print(len(self.cpu_usage_search))
        else:
            print('data tidak ada')

    # menyimpan data list penggunaan CPU ke dalam file biner
    def saveData(self):
        dump(self.cpu_usage_publish, 'cpu usage publish.jlb')
        dump(self.mean_publish, 'mean cpu usage publish.jlb')
        dump(self.cpu_usage_search, 'cpu usage search.jlb')
        dump(self.mean_search, 'mean cpu usage search.jlb')

        file = open('mean cpu usage publish.txt', 'w')
        file.write(str(self.mean_publish))
        file.close()

        file = open('mean cpu usage search.txt', 'w')
        file.write(str(self.mean_search))
        file.close()

        file = open('cpu usage publish time.txt', 'w')
        file.write(str(self.publish_time))
        file.close()

        file = open('cpu usage search time.txt', 'w')
        file.write(str(self.search_time))
        file.close()

        file = open('list miner.txt', 'w')
        file.write(str(self.list_miner))
        file.close()

        file = open('final mean.txt', 'w')
        file.write('final mean publish: ' + str(self.final_mean_publish))
        file.write('\nfinal mean search: ' + str(self.final_mean_search))
        file.write('\nfinal publish time: ' + str(self.final_publish_time))
        file.write('\nfinal search time: ' + str(self.final_search_time))
        file.close()

    # membaca data list penggunaan CPU dari file biner
    def readData(self):
        self.cpu_usage_publish = load('cpu usage publish.jlb')
        self.mean_publish = load('mean cpu usage publish.jlb')
        self.cpu_usage_search = load('cpu usage search.jlb')
        self.mean_search = load('mean cpu usage search.jlb')

