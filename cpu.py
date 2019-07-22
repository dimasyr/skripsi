import matplotlib.pyplot as plt
import psutil as psu

i = 0
cpu = []
while i != 10:
    cpu.append(psu.cpu_percent(1))
    i += 1

# red dashes, blue squares and green triangles
plt.plot(cpu, 'r--')
plt.show()