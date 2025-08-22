import torch

# 定义变量
x = torch.tensor(1.0, requires_grad=True)
y = torch.tensor(2.0, requires_grad=True)

# 定义函数 f(x,y) = x^2 + x*y + y^2
f = x**2 + x*y + y**2

# -------- 直接计算 Hessian --------
# 对每个参数分别求一阶梯度
import pdb; pdb.set_trace()
grads = torch.autograd.grad(f, (x, y), create_graph=True)
# grads = (df/dx, df/dy)

H_rows = []
for g in grads:  # 对每个一阶梯度再求梯度
    row = torch.autograd.grad(g, (x, y), retain_graph=True)
    H_rows.append(torch.stack(row))

H = torch.stack(H_rows)
print("Hessian 矩阵:\n", H)

# -------- 验证 Hv --------
v = torch.tensor([1.0, 2.0])   # 任意向量
Hv = H @ v
print("Hv (直接矩阵乘法):", Hv)

# -------- 用 Pearlmutter trick 计算 Hv --------
grad_vec = torch.autograd.grad(f, (x, y), create_graph=True)
grad_vec = torch.cat([g.view(-1) for g in grad_vec])
dot = torch.dot(grad_vec, v)  # g^T v
Hv_trick = torch.autograd.grad(dot, (x, y))
Hv_trick = torch.cat([h.view(-1) for h in Hv_trick])
print("Hv (autograd trick):", Hv_trick)
