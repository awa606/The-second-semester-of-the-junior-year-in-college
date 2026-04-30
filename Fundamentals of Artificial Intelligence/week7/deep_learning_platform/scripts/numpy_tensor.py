import torch
import numpy as np

# 1. 基本定义
print("1. 基本定义对比")
print("=" * 50)

# NumPy数组
np_array = np.array([[1, 2, 3], [4, 5, 6]])
print(f"NumPy数组:\n{np_array}")
print(f"类型: {type(np_array)}")
print(f"形状: {np_array.shape}")
print(f"数据类型: {np_array.dtype}")
print(f"设备: CPU (固定)")

# PyTorch Tensor
torch_tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"\nPyTorch Tensor:\n{torch_tensor}")
print(f"类型: {type(torch_tensor)}")
print(f"形状: {torch_tensor.shape}")
print(f"数据类型: {torch_tensor.dtype}")
print(f"设备: {torch_tensor.device}")