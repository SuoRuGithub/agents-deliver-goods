#coding=gbk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ʾ�����ݣ�M ��С������ N ��ʱ�䲽������λ��
AGENT_NUM = 10  # С��������
STEPS = 50  # ʱ�䲽����

# ��������� M*N ����ÿ��Ԫ����һ����Ԫ�飨x, y������
data = np.random.rand(AGENT_NUM, STEPS, 2) * 10  # ��Χ�� 0 �� 10 ֮�������
fig, ax = plt.subplots()
scatters = [ax.plot([], [], 'o')[0] for _ in range(M)]  # 

ax.set_xlim(0, 32)
ax.set_ylim(0, 10)

def init():
    for scatter in scatters:
        scatter.set_data([], [])
    return scatters

def update(frame):
    for i, scatter in enumerate(scatters):
        scatter.set_data(data[i, frame, 0], data[i, frame, 1])
    return scatters

ani = animation.FuncAnimation(fig, update, frames=N, init_func=init, blit=True)

plt.show()