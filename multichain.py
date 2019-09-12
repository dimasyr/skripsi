from Savoir import Savoir
import time
import threading
from recordCPU import RecordCPU

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

        self.CPU = RecordCPU()
        # self.cpu_usage_publish = []
        # self.cpu_usage_search = []
        # self.is_mining = False
        # self.record_cpu = False
        # self.search_results = []

        self.initApi()

    def initApi(self):
        '''

        :return:
        '''
        self.api = Savoir(self.rpcuser, self.rpcpassword, self.rpchost, self.rpcport, self.chainname)

    # param stream (nama stream), num (jumlah data yg ingin di return)
    def listStreamItems(self, stream, num=0, isSearch = False):
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

        if(isSearch):
            self.CPU.search_results = items
            print(self.CPU.search_results)
        else:
            return items

    def searchItem(self, stream, num=0):
        def record():
            return self.CPU.recordCpuUsage('search')

        def search():
            return self.listStreamItems(stream, num, True)

        self.CPU.is_mining = True
        self.CPU.record_cpu = True

        threading.Thread(target = record).start()
        time.sleep(3)
        threading.Thread(target = search).start()

        time.sleep(3)
        self.CPU.is_mining = False
        self.CPU.record_cpu = False

    # belum selesai (untuk melihat detail item)
    def getStreamItems(self, stream, num):
        item = self.listStreamItems(stream, num)

        data = self.api.getstreamitem(stream)
        return data

    # mendapatkan info miner
    def getMiner(self, txid):
        data = self.api.getwallettransaction(txid)
        block = self.api.getblock(data['blockhash'])
        return block['miner']

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

        def streamData():
            return self.isMined(stream, data)

        def record():
            return self.CPU.recordCpuUsage('publish')

        self.CPU.is_mining = True
        self.CPU.record_cpu = True

        threading.Thread(target = record).start()
        time.sleep(3)
        self.api.publish(stream, key, data)
        threading.Thread(target = streamData).start()

        proses = ''

        while True:
            if self.CPU.is_mining == False:
                proses = 'done'
                break

        return proses

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
        start = time.time()

        print('\nStream last item data = ' + str(items[0]['data']))
        print('Stream last item confirmations = ' + str(items[0]['confirmations']))

        # mengecek item terakhir (terbaru) apakah sudah di mining
        while (items[0]['confirmations'] == 0):
            items = self.listStreamItems(stream, 1)

        # waktu saat item terakhir (terbaru) sudah di mining
        end = time.time()
        time.sleep(3)
        self.CPU.record_cpu = False
        self.CPU.is_mining = False

        # mendapatkan durasi proses mining
        mining_time = end - start

        print('\nStream last item data = ' + str(items[0]['data']))
        print('Stream last item confirmations : ' + str(items[0]['confirmations']))
        print('Waktu mining = ' + str(mining_time))

# if __name__ == '__main__':
#     Chain1 = Multichain('multichainrpc', '44hCoTauwmQTSxtvQ9au99QqzjBs6pkPriqayqjYqF6f', 'localhost', '7172', 'chain1')

    # items = Chain1.listStreamItems('stream1', 12)
    #
    # for i in range(len(items)):
    #     print(items[i]['data'])

    # miner = Chain1.getMiner(items[0]['txid'])
    # print(miner)

    # Chain1.printData(items, True)
    # print(items[0]['data'])