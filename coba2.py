# import threading, time, queue
#
# class coba:
#     def tambahx(self, x):
#         total = 0
#         for i in range(5):
#             total += int(x)
#             time.sleep(1)
#
#         print(total)
#
#     def tambahy(self, y):
#         total = 0
#         for i in range(5):
#             total += int(y)
#             time.sleep(1)
#
#         print(total)
#
# hasil = queue.Queue()
# tes = coba()
#
# threading.Thread(target=tes.tambahx, args='1').start()
# threading.Thread(target=tes.tambahy, args='2').start()

import threading
import queue

class coba:
    def dosomething(self, param, param2):
        return param * 2 + param2

que = queue.Queue()
x = coba()

thr = threading.Thread(target = lambda q, arg : q.put(x.dosomething(arg)), args = (que, 5, 2))
thr.start()
thr.join()

while not que.empty():
    print(que.get())