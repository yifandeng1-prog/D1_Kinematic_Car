import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 参数
# -----------------------------
L = 2.5       # 轴距
DT = 0.1      # 时间步长
STEPS = 300   # 仿真步数

# 设置打印格式
np.set_printoptions(precision=3, suppress=True)

# -----------------------------
# 状态更新函数
# -----------------------------
def update(state, action):
    x, y, yaw, v = state
    a, delta = action
    x_next = x + v * np.cos(yaw) * DT
    y_next = y + v * np.sin(yaw) * DT
    yaw_next = yaw + v / L * np.tan(delta) * DT
    v_next = v + a * DT
    return np.array([x_next, y_next, yaw_next, v_next])

# -----------------------------
# 仿真循环
# -----------------------------
state = np.array([0.0, 0.0, 0.0, 1.0])
traj = []

# 固定输入
acceleration = 0.02
steering_angle_deg = 10
steering_angle = np.deg2rad(steering_angle_deg)

for _ in range(STEPS):
    action = np.array([acceleration, steering_angle])
    state = update(state, action)
    traj.append(state.copy())

traj = np.array(traj)

# -----------------------------
# 分离轨迹数据
# -----------------------------
xs = traj[:,0]
ys = traj[:,1]
yaws = traj[:,2]
vs = traj[:,3]

# -----------------------------
# 打印前10步状态
# -----------------------------
print("前10步状态:")
for i in range(10):
    print(f"Step {i}: x={xs[i]:.3f}, y={ys[i]:.3f}, yaw={yaws[i]:.3f}, v={vs[i]:.3f}")

# -----------------------------
# 创建保存图片文件夹
# -----------------------------
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)

# -----------------------------
# 画图
# -----------------------------
# 1. 平面轨迹
plt.figure(figsize=(6,6))
plt.plot(xs, ys, label=f"delta={steering_angle_deg}°")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Kinematic Car Trajectory")
plt.axis("equal")
plt.grid(True)
plt.savefig(os.path.join(fig_dir, "trajectory.png"))
plt.show()

# 2. 速度随时间变化
plt.figure()
plt.plot(np.arange(STEPS)*DT, vs, color='orange')
plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s]")
plt.title("Velocity over Time")
plt.grid(True)
plt.savefig(os.path.join(fig_dir, "velocity.png"))
plt.show()

# 3. 航向角随时间变化
plt.figure()
plt.plot(np.arange(STEPS)*DT, yaws, color='green')
plt.xlabel("Time [s]")
plt.ylabel("Yaw [rad]")
plt.title("Yaw over Time")
plt.grid(True)
plt.show()