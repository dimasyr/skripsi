from Savoir import Savoir
import time, psutil
import threading
import matplotlib.pyplot as plt

class Multichain:
    '''

    '''

    def __init__(self, rpcuser, rpcpassword, rpchost, rpcport, chainname):
        '''

        :param rpcuser:
        :param rpcpassword:
        :param rpchost:
        :param rpcport:
        :param chainname:
        '''
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.rpchost = rpchost
        self.rpcport = rpcport
        self.chainname = chainname
        self.cpu_usage = []
        self.is_mining = False
        self.record_cpu = False

        self.initApi()

    def initApi(self):
        '''

        :return:
        '''
        self.api = Savoir(self.rpcuser, self.rpcpassword, self.rpchost, self.rpcport, self.chainname)

    #         param stream (nama stream), num (jumlah data yg ingin di return)
    def listStreamItems(self, stream, num=0):
        '''

        :param stream:
        :param num:
        :return:
        '''
        if num == 0:
            items = self.api.liststreamitems(stream)
        else:
            items = self.api.liststreamitems(stream)
            items = items[-num:]
        return items

# belum selesai
    def getStreamItems(self, stream, num):
        item = self.listStreamItems(stream, num)

        data = self.api.getstreamitem(stream)
        return data

    def getStreamInfo(self, stream):
        '''

        :param stream:
        :return:
        '''
        return self.api.getstreaminfo(stream)

    #         param opt1 (print data), opt (print confirmations)
    def printData(self, items, data = False, confirm = False, txid = False, all = True):
        '''

        :param items:
        :param opt1:
        :param opt2:
        :return:
        '''
        total_item = len(items)
        for x in range(total_item):
            if data :
                print(bytes.fromhex(items[x]['data']).decode('utf-8'))
                all = False
            if confirm :
                print(items[x]['confirmations'], '\n')
                all = False
            if txid:
                print(items[x]['txid'], '\n')
                all = False
            if all :
                print(items[x], '\n')

    def publishStream(self, stream, key, data):
        '''

        :param stream:
        :param key:
        :param data:
        :return:
        '''

        self.api.publish(stream, key, data)
        self.is_mining = True
        def streamData():
            return self.isMined(stream, data)

        threading.Thread(target = streamData).start()
        threading.Thread(target = self.recordCpuUsage).start()

    def isMined(self, stream, data):
        '''

        :param stream:
        :param data:
        :return:
        '''

        global items

        # mendapatkan item terakhir (terbaru) dalam streams
        items = self.listStreamItems(stream, 1)

        # mengecek apakah item terakhir (terbaru) sama dengan data inputan terakhir
        while (items[0]['data'] != data):
            items = self.listStreamItems(stream, 1)

        # waktu awal item terakhir (terbaru) masuk ke dalam stream
        self.record_cpu = True
        start = time.time()

        print('\nStream last item data = ' + str(items[0]['data']))
        print('Stream last item confirmations = ' + str(items[0]['confirmations']))

        # mengecek item terakhir (terbaru) apakah sudah di mining
        while (items[0]['confirmations'] == 0):
            items = self.listStreamItems(stream, 1)

        # waktu saat item terakhir (terbaru) sudah di mining
        end = time.time()
        self.record_cpu = False
        self.is_mining = False

        # mendapatkan durasi proses mining
        mining_time = end - start

        print('\nStream last item data = ' + str(items[0]['data']))
        print('Stream last item confirmations : ' + str(items[0]['confirmations']))
        print('Waktu mining = ' + str(mining_time))

    def recordCpuUsage(self):
        while self.is_mining:
            global temp
            temp = []

            while self.record_cpu:
                temp.append(psutil.cpu_percent(0.1))

            if len(temp) != 0:
                self.cpu_usage.append(temp)

    def printCpuUsage(self):
        if len(self.cpu_usage) != 0:
            for i in range(len(self.cpu_usage)):
                plt.plot(self.cpu_usage[i], 'r--')
                plt.show()
        else:
            print('data belum ada')

    def lenCPU(self):
        print(len(self.cpu_usage))

# if __name__ == '__main__':
#     Chain1 = Multichain('multichainrpc', '44hCoTauwmQTSxtvQ9au99QqzjBs6pkPriqayqjYqF6f', 'localhost', '7172', 'chain1')
#
#     items = Chain1.listStreamItems('stream1', 1)
    #
    # Chain1.printData(items, True)
    # print(items[0]['data'])