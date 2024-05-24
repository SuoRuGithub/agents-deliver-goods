#coding=gbk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 示例数据：M 个小方块在 N 个时间步的坐标位置
AGENT_NUM = 10  # 小方块数量
STEPS = 50  # 时间步数量

# 生成随机的 M*N 矩阵，每个元素是一个二元组（x, y）坐标
data = np.random.rand(AGENT_NUM, STEPS, 2) * 10  # 范围在 0 到 10 之间的坐标
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