import threading, time

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
    tes = coba()

    threading.Thread(target=tes.tambahx, args='1').start()
    threading.Thread(target=tes.tambahy, args='2').start()

    while 1:
        print('hokya')
        time.sleep(1)
