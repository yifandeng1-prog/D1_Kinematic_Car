import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 参数
# -----------------------------
L = 2.5       # 轴距
DT = 0.05     # 时间步长（更小，轨迹更平滑）
STEPS = 300   # 仿真步数

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
# 小车跟踪目标点（平滑版本）
# -----------------------------
def compute_steering(state, target, Kp=0.5):
    """
    简单比例控制：
    delta = Kp * (期望航向 - 当前航向)
    限制在 [-30°, 30°]
    """
    x, y, yaw, _ = state
    x_goal, y_goal = target
    dx = x_goal - x
    dy = y_goal - y
    desired_yaw = np.arctan2(dy, dx)
    delta = desired_yaw - yaw
    delta = np.arctan2(np.sin(delta), np.cos(delta))  # 归一化到 [-pi, pi]
    delta = np.clip(Kp * delta, np.deg2rad(-30), np.deg2rad(30))
    return delta

# -----------------------------
# 仿真初始化
# -----------------------------
state = np.array([0.0, 0.0, 0.0, 1.0])
traj = []

acceleration = 0.02
x_goal, y_goal = 10.0, 10.0

for _ in range(STEPS):
    delta = compute_steering(state, (x_goal, y_goal))
    action = np.array([acceleration, delta])
    state = update(state, action)
    traj.append(state.copy())

traj = np.array(traj)
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
# 平面轨迹
plt.figure(figsize=(6,6))
plt.plot(xs, ys, label="Trajectory")
plt.plot(x_goal, y_goal, "ro", label="Goal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Kinematic Car Smooth Trajectory to Goal")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(fig_dir, "trajectory_to_goal_smooth.png"))
plt.show()

# 速度变化
plt.figure()
plt.plot(np.arange(STEPS)*DT, vs, color='orange')
plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s]")
plt.title("Velocity over Time")
plt.grid(True)
plt.savefig(os.path.join(fig_dir, "velocity_smooth.png"))
plt.show()

# 航向角变化
plt.figure()
plt.plot(np.arange(STEPS)*DT, yaws, color='green')
plt.xlabel("Time [s]")
plt.ylabel("Yaw [rad]")
plt.title("Yaw over Time")
plt.grid(True)
plt.show()