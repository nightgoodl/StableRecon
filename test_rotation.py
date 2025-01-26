import numpy as np

# 元数据中的旋转矩阵
rotation_metadata = np.array([
    [-0.03876108676195145, 0.8529655337333679, 0.5205252766609192],
    [-0.6662989258766174, 0.3661441504955292, -0.6496028900146484],
    [-0.7446765899658203, -0.3720049262046814, 0.5541381239891052]
])

# 算法计算的旋转矩阵
rotation_algorithm = np.array([
    [0.6243, -0.7194, 0.3045],
    [0.3320, -0.1085, -0.9370],
    [0.7071, 0.6861, 0.1711]
])

# 计算相对旋转矩阵
relative_rotation = rotation_metadata @ rotation_algorithm.T

# 检查相对旋转矩阵是否接近单位矩阵
print("Relative Rotation Matrix:")
print(relative_rotation)

# 计算相对旋转的角度
angle = np.arccos((np.trace(relative_rotation) - 1) / 2)
print(f"Angle difference: {np.degrees(angle):.2f} degrees")