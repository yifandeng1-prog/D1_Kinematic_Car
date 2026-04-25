# D1 Kinematic Car Simulation

## Goal
Use Python and NumPy to simulate a 2D kinematic car model.

## State
**什么是 state？**  
State 表示机器人当前的状态信息。在这个小车模型中，state 包含 `[x, y, yaw, v]`，分别表示小车在世界坐标系的位置、航向角和速度。它记录了系统在某一时刻的完整信息，用于下一步状态更新。

## Action / Control Input
**什么是 action/control input？**  
Action 是控制输入，用于改变机器人状态。在我们的代码中，action 包含 `[acceleration, delta]`，分别表示加速度和转向角。通过给定 action，系统可以产生新的状态。

## Dynamics
**什么是 dynamics？**  
Dynamics 描述 state 如何随 action 变化。在这个小车模型里，update() 函数就是 dynamics，它根据公式计算下一步的 `[x_next, y_next, yaw_next, v_next]`。Dynamics 是状态更新的核心机制。

## 为什么轨迹是由循环状态更新产生的？
轨迹是由每一步 state 按时间顺序连接起来形成的。在代码中，我们用 for 循环不断调用 update()，每一步得到新的 state 并保存到列表中。循环状态更新自然生成完整的运动轨迹。

## 这个小车模型和机器人/无人机/自动驾驶有什么关系？
这个小车模型是具身智能最基础的入门案例。无论是移动机器人、无人机还是自动驾驶车辆，都需要 state → action → next state 的闭环接口。通过理解小车运动学，可以为 PID、MPC、强化学习等控制方法打基础。