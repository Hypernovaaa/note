<p align="center"> <img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250814/image.8vn8lj7em7.jpg" width=800> </p>

## 参考资源
- [flashattn 论文地址](https://arxiv.org/pdf/2205.14135)

## 标准情况下的attention实现
- attention需要的输入首先存储在HBM中, KQV的shape为[batch, seq_eln, dim], 并且这里的seq_len一般是远大于dim的, dim长度一般是64或者128, 但是序列长度一般是2k起步, 有的模型支持上万的上下文长度. 根据自注意力的计算公式
$$\begin{align}
Attention(QKV) = softmax\{\frac{Q * K^T}{\sqrt{d}}\} * V
\end{align}$$
- 1. 将Q和K从HBM加载到SRAM中, 计算$S=Q*K^T$, 将S写回到HBM中. 以A100的20M的Sram为例,可以支持的单个fp32 Q的序列长度为$\frac{20 * 1024 * 1024}{4 * 128}=40,960$ , 可见sram大部分情况下可以支撑把K和Q都加载进去, 但是S的维度为[seq_len, seq_len], 20M的sram可以支撑的S的最大序列长度为$\sqrt{\frac{20*1024*1024}{4}} = 2290$, 这时sram中还有K和Q,以及一些其他的中间结果, 所以不可能再把S矩阵存储在Sram上了, 只能是写入到HBM
- 2. 因为Sram放不下整个S矩阵, 并且softmax是按照行做的, 因此这里会一次读入S矩阵的几行做softmax, 做完softmax的结果也要存回HBM中形成P矩阵
- 3. 从HBM中加载P和V做常规的矩阵乘法, 最后输出O与V的维度相同, 写入到HBM中
- 4. 返回self-attention结果O

# Flashattn 自注意力实现
- Flashattn的核心思想是通过分段计算softmax, 尽可能一次读取Q,K就拿到想要的结果, 通过减少HBM的访问提升计算速度
## tilling分段计算softmax
- 基础的softmax计算公式如下, $X \in \mathbb{R}^n$:
$$\begin{align}
softmax(X) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}
\end{align}$$
- 如果$x_i$接近$-\infty$会使梯度接近0, 导致模型学习变慢, 如果$x_i$太大又会导致数值上溢, softmax退化到hardmax, 导致梯度尖锐并且训练不稳定, 因此在实际使用的时候会使用以下safe softmax函数, m表示$X$中的最大值:
$$\begin{align}
softmax(X) = \frac{e^{x_i - m}}{\sum_{j} e^{x_j - m}}
\end{align}$$

- 分段式计算softmax, 以分两段计算为例此时$X = [X_1, X_2], X_1,X_2 \in R^{2n}$, $X_1$中的最大值为$m_1$, $X_2$中的最大值为$m_2$, 整体的最大值依旧为$m$, 对第一段的局部softmax计算结果为
$$\begin{align}
softmax(X_1) = \frac{e^{x_i - m_1}}{\sum_{j}e^{x_j - m_1}}
\end{align}$$

- 这里距离真正的softmax结果就是将$m_1$替换成$m$, 因此乘以因子$e^{m1 - m}$
