from Savoir import Savoir
import time

class Multichain:

    def __init__(self, rpcuser, rpcpassword, rpchost, rpcport, chainname):
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.rpchost = rpchost
        self.rpcport = rpcport
        self.chainname = chainname

        self.initApi()

    def initApi(self):
        self.api = Savoir(self.rpcuser, self.rpcpassword, self.rpchost, self.rpcport, self.chainname)

    #         param stream (nama stream), num (jumlah data yg ingin di return)
    def getStreamItems(self, stream, num=0):
        if num == 0:
            items = self.api.liststreamitems(stream)
        else:
            items = self.api.liststreamitems(stream)
            items = items[-num:]
        return items

    def getStreamInfo(self, stream):
        return self.api.getstreaminfo(stream)

    #         param opt1 (print data), opt (print confirmations)
    def printData(self, items, opt1='', opt2=''):
        total = len(items)
        for x in range(total):
            if opt1 == 'data':
                print(bytes.fromhex(items[x]['data']).decode('utf-8'))
            if opt2 == 'confirmations':
                print(items[x]['confirmations'], '\n')
            if (opt1 == '' and opt2 == ''):
                print(items[x], '\n')

    def publishStream(self, stream, key, data):
        self.api.publish(stream, key, data)
        self.isMined(stream, data)

    def isMined(self, stream, data):
        # mendapatkan item terakhir (terbaru) dalam streams
        items = self.getStreamItems(stream, 1)

        # mengecek apakah item terakhir (terbaru) sama dengan data inputan terakhir
        while (items['data'] != data):
            items = self.getStreamItems(stream, 1)

        # waktu awal item terakhir (terbaru) masuk ke dalam stream
        start = time.time()

        print('\nStream last item data = ' + str(items['data']))
        print('Stream last item confirmations = ' + str(items['confirmations']))

        # mengecek item terakhir (terbaru) apakah sudah di mining
        while (items['confirmations'] == 0):
            items = self.getStreamItems(stream, 1)

        # waktu saat item terakhir (terbaru) sudah di mining
        end = time.time()

        # mendapatkan durasi proses mining
        mining_time = end - start

        print('\nStream last item data = ' + str(items['data']))
        print('Stream last item confirmations : ' + str(items['confirmations']))
        print('Waktu mining = ' + str(mining_time))

Chain1 = Multichain('multichainrpc', '44hCoTauwmQTSxtvQ9au99QqzjBs6pkPriqayqjYqF6f', 'localhost', '7172', 'chain1')

items = Chain1.getStreamItems('stream1', 6)

Chain1.printData(items, 'data', 'confirmations')