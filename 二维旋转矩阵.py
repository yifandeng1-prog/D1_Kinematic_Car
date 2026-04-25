#world_point=robot_position+R(θ)⋅local_point

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 核心部分：手写实现旋转矩阵
# ==========================================
def get_rotation_matrix(theta_degrees):
    """
    输入角度（度），输出2x2旋转矩阵
    """
    theta = np.radians(theta_degrees)  # 转换成弧度
    
    # 【关键】这里必须按照推导的位置写，不能错！
    R = np.array([
        [np.cos(theta), -np.sin(theta)],  # 第一行：cos, -sin
        [np.sin(theta),  np.cos(theta)]   # 第二行：sin,  cos
    ])
    return R

# ==========================================
# 2. 设定初始参数
# ==========================================
# 机器人在世界坐标系的位置 (x, y)
robot_pos = np.array([2, 2])

# 一个在机器人局部坐标系中的点：在机器人正前方偏左一点
# 我们把它定义为一个"L"形，方便看旋转效果
local_points = np.array([
    [0, 1, 1, 0.5, 0.5, 0, 0],  # 局部X坐标
    [0, 0, 1, 1, 0.5, 0.5, 0]   # 局部Y坐标
])

# ==========================================
# 3. 测试函数：计算并画图
# ==========================================
def test_rotation(theta_deg, ax):
    # 1. 获取旋转矩阵
    R = get_rotation_matrix(theta_deg)
    
    # 2. 执行公式：world = robot_pos + R @ local
    # 注意：这里用了广播机制，对所有点同时计算
    world_points = robot_pos.reshape(2, 1) + R @ local_points
    
    # 3. 绘图
    # 绘制机器人（用黑色箭头表示朝向）
    ax.scatter(robot_pos[0], robot_pos[1], color='black', s=100, label='Robot')
    # 画一个简单的箭头表示机器人朝向
    arrow_dir = R @ np.array([[0.5], [0]])
    ax.arrow(robot_pos[0], robot_pos[1], 
             arrow_dir[0, 0], arrow_dir[1, 0],
             head_width=0.1, fc='black', ec='black')
    
    # 绘制局部坐标系下的形状（仅作参考，放在原点旁边）
    ax.fill(local_points[0, :], local_points[1, :], 
            color='lightblue', alpha=0.3, label='Local Shape (Origin)')
    ax.plot(local_points[0, :], local_points[1, :], 
            color='blue', linewidth=1, linestyle='--')
    
    # 绘制世界坐标系下旋转后的形状
    ax.fill(world_points[0, :], world_points[1, :], 
            color='lightcoral', alpha=0.5, label=f'World Shape (Rotated {theta_deg}°)')
    ax.plot(world_points[0, :], world_points[1, :], 
            color='red', linewidth=2)
    
    # 美化图表
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5)
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')
    ax.set_title(f'Test: Theta = {theta_deg}°')
    ax.legend(loc='lower right')

# ==========================================
# 4. 主程序：分别测试 30°, 60°, 90°
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

test_rotation(30, ax1)
test_rotation(60, ax2)
test_rotation(90, ax3)

plt.tight_layout()
plt.show()

print("测试完成！请查看生成的图片。")
print("\n验收知识点回顾：")
print("1. 世界坐标系：固定不动的全局参考系。")
print("2. 机器人坐标系：以机器人为中心，随机器人移动旋转的参考系。")
print("3. 旋转矩阵作用：将局部坐标投影到世界坐标系的方向上。")