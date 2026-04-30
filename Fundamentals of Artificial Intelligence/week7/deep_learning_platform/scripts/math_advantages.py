import torch

def mathematical_advantages():
    """Tensor的数学优势"""

    # 1. 统一的数学运算
    A = torch.randn(3, 4)
    B = torch.randn(4, 5)
    C = torch.randn(3, 4)

    # 矩阵乘法
    matmul = torch.matmul(A, B)
    print(matmul.shape)

    # 逐元素运算
    elementwise = A * C
    print(elementwise.shape)

    # 广播机制
    scalar = torch.tensor(2.0)
    broadcasted = A + scalar  # 自动扩展到A的形状
    print(scalar.shape)
    print(broadcasted.shape)

    # 2. 张量缩并 (Tensor Contraction)
    # 爱因斯坦求和约定
    x = torch.randn(3, 4, 5)
    y = torch.randn(5, 6, 7)

    # 在特定维度上求和
    result = torch.einsum('ijk,klm->ijlm', [x, y])
    print(result.shape)

    return matmul, elementwise, broadcasted, result


if __name__ == "__main__":
    mathematical_advantages()