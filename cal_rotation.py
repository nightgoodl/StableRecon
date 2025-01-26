import numpy as np

def rotation_matrix_to_euler_zyx(R):
    """将旋转矩阵转换为ZYX顺序的欧拉角（弧度）"""
    pitch = np.arcsin(-R[2, 0])
    if np.abs(np.cos(pitch)) > 1e-6:
        yaw = np.arctan2(R[1, 0], R[0, 0])
        roll = np.arctan2(R[2, 1], R[2, 2])
    else:
        # 处理万向节锁（θ ≈ ±90°）
        yaw = 0
        roll = np.arctan2(-R[0, 1], R[1, 1])
    return np.array([yaw, pitch, roll])

def rotation_matrix_to_axis_angle(R):
    """将旋转矩阵转换为轴-角表示"""
    theta = np.arccos((np.trace(R) - 1) / 2)
    if np.abs(theta) < 1e-6:
        return np.array([0, 0, 1]), 0  # 无旋转，默认Z轴
    elif np.abs(theta - np.pi) < 1e-6:
        # θ = π，旋转轴需特殊计算
        u = np.sqrt((np.diag(R) + 1) / 2)
        u /= np.linalg.norm(u)
        return u, theta
    else:
        u = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1]
        ]) / (2 * np.sin(theta))
        return u, theta

# 示例矩阵
R_meta = np.array([
          [
            -0.3184819519519806,
            0.9476474523544312,
            0.023106934502720833
          ],
          [
            0.4135854244232178,
            0.16084741055965424,
            -0.8961443901062012
          ],
          [
            -0.8529455065727234,
            -0.2758490741252899,
            -0.44316011667251587
          ]
])

# 计算欧拉角（ZYX顺序）
yaw, pitch, roll = rotation_matrix_to_euler_zyx(R_meta)
print(f"欧拉角 (ZYX): Yaw={np.degrees(yaw):.2f}°, Pitch={np.degrees(pitch):.2f}°, Roll={np.degrees(roll):.2f}°")

# 计算轴-角表示
u, theta = rotation_matrix_to_axis_angle(R_meta)
print(f"轴-角: 轴={u}, 角度={np.degrees(theta):.2f}°")