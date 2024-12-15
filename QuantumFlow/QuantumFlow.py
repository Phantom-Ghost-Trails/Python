import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np

# 初始化图形对象
fig, ax = plt.subplots(figsize=(10, 6))

# 创建一个列表来保存x轴和y轴的数据
x = []
y1 = []
y2 = []
y3 = []

# 设置最大数据点数量
max_points = 100

# 定义一个函数来生成新的数据点
def animate(i):
    x.append(i)  # x轴值为时间点
    new_y1 = random.randint(1, 100)  # 第一个y轴值为随机整数
    new_y2 = np.sin(i / 10.0) * 100 + 50  # 第二个y轴值基于正弦波
    new_y3 = np.cos(i / 10.0) * 100 + 50  # 第三个y轴值基于余弦波
    y1.append(new_y1)
    y2.append(new_y2)
    y3.append(new_y3)
    
    # 限制数据点的数量
    if len(x) > max_points:
        x.pop(0)
        y1.pop(0)
        y2.pop(0)
        y3.pop(0)
    
    # 动态调整X轴和Y轴的刻度范围
    ax.set_xlim(max(0, i - max_points + 1), i + 1)
    ax.set_ylim(min(min(y1), min(y2), min(y3)) - 10, max(max(y1), max(y2), max(y3)) + 10)
    
    # 更新数据系列
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    
    # 添加顶部静态注释
    fig.text(0.5, 0.95, f'当前时间点: {i}', ha='center', va='center', fontsize=12, color='black')
    
    # 添加右侧动态注释
    ax.annotate(f'随机数据: {new_y1:.2f}', xy=(1, 1), xycoords='axes fraction', xytext=(-10, -10),
                textcoords='offset points', ha='right', va='top', fontsize=10, color='blue')
    ax.annotate(f'正弦波数据: {new_y2:.2f}', xy=(1, 0.95), xycoords='axes fraction', xytext=(-10, -10),
                textcoords='offset points', ha='right', va='top', fontsize=10, color='red')
    ax.annotate(f'余弦波数据: {new_y3:.2f}', xy=(1, 0.9), xycoords='axes fraction', xytext=(-10, -10),
                textcoords='offset points', ha='right', va='top', fontsize=10, color='green')
    
    return line1, line2, line3

# 初始化线条
line1, = ax.plot([], [], label='随机数据', color='blue')  # 绘制第一个数据系列
line2, = ax.plot([], [], label='正弦波数据', linestyle='--', color='red')  # 绘制第二个数据系列
line3, = ax.plot([], [], label='余弦波数据', linestyle=':', color='green')  # 绘制第三个数据系列

# 设置背景颜色和网格
ax.set_facecolor('#f0f0f0')
ax.grid(True, linestyle='--', alpha=0.7)

# 显示图例
ax.legend()

# 设置标题和标签
ax.set_title('动态图表示例')
ax.set_xlabel('时间点')
ax.set_ylabel('数值')

# 设置动画
ani = animation.FuncAnimation(fig, animate, frames=200, interval=200, blit=True, repeat=False)

# 显示图形
plt.show()
