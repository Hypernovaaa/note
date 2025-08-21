# 简介
- Actor-Critic当策略网络是深度模型时，沿着策略梯度更新参数，很有可能由于步长太长，策略突然显著变差，进而影响训练效果
- 在更新时找到一块信任区域（trust region），在这个区域上更新策略时能够得到某种策略性能的安全性保证，这就是信任区域策略优化（trust region policy optimization，TRPO）算法的主要思想
# 策略目标
- 当前策略为$\pi_\theta$，参数为$\theta$，目标是找到更优的参数$\theta'$，使$\mathcal{J}(\theta') \ge \mathcal{J}(\theta)$，由于初始状态$s_0$的分布和策略无关，因此上述策略$\pi_\theta$下的优化目标可以写成在新策略$\pi_{\theta'}$的期望的形式
	$$\begin{align}
	\mathcal{J}(\theta) &= \mathbb{E}_{s_0}[V^{\pi_\theta}(s_0)] \\
	% &= \mathbb{E}_{\pi_\theta} \left[\sum_{t=0}^\infty \gamma^t V^{\pi_\theta}(s_t)\right] \\
	&= \mathbb{E}_{\pi_{\theta'}}\left[\sum_{t=0}^\infty \gamma^t V^{\pi_\theta}(s_t) - \sum_{t=1}^\infty \gamma^t V^{\pi_\theta}(s_t) \right] \\
	&= -\mathbb{E}_{\pi_{\theta'}}\left[\sum_{t=0}^\infty \gamma^t(\gamma V^{\pi_\theta}(s_{t+1}) - V^{\pi_\theta}(s_t) \right]
	\end{align}$$
	- 这里公式1到公式2中$V^{\pi_\theta}(s_0)$和$(\sum_{t=0}^\infty \gamma^t V^{\pi_\theta}(s_t) - \sum_{t=1}^\infty \gamma^t V^{\pi_\theta}(s_t))$是完全等价的，但是期望的下标为什么从$s_0$变成了$\pi_{\theta'}$？（个人理解）
		- 首先公式1中$s_0$是一个随机变量，这个是环境决定的，我们玩一局游戏的初始状态只跟这个游戏本身有关，跟策略无关，那这个期望就是环境给出初始状态的分布，计算这个初始状态价值的期望
		- 公式2中$(\sum_{t=0}^\infty \gamma^t V^{\pi_\theta}(s_t) - \sum_{t=1}^\infty \gamma^t V^{\pi_\theta}(s_t))$含义是采样了一条序列但是只取0时刻的状态价值，这里“关于随机变量$\tau$的期望”这个$\tau$的含义从环境给的随机变量变成了我们采样测序列，因此下标变成了新策略$\pi_{\theta'}$
		- 因为初始状态的分布和策略无关，所以这里用什么策略都可以，这里就变成了旧策略对新策略采样下的初始状态的价值的期望
- 新旧策略目标函数之差为
	$$\begin{align}
	\mathcal{J}(\theta') - \mathcal{J}(\theta) &= \mathbb{E}_{s_0}[V^{\pi_{\theta'}}(s_0)] - \mathbb{E}_{s_0}[V^{\pi_\theta}(s_0)] \\
	&= \mathbb{E}_{\pi_{\theta'}}\left[\sum_{t=0}^\infty \gamma^t r(s_t, a_t)\right] + \mathbb{E}_{\pi_{\theta'}} \left[\sum_{t=0}^\infty \gamma^t(\gamma V^{\pi_\theta}(s_{t+1}) - V^{\pi_\theta}(s_t) \right]\\
	&= \mathbb{E}_{\pi_{\theta'}}\left[\sum_{t=0}^\infty \gamma^t[r(s_t, a_t) + \gamma V^{\pi_\theta}(s_{t+1}) - V^{\pi_\theta}(s_t)]\right]\\
	&= \mathbb{E}_{\pi_{\theta'}}\left[\sum_{t=0}^\infty \gamma^t A^{\pi_\theta}(s_t, a_t)\right]\\
	&= \sum_{t=0}^\infty \gamma^t \mathbb{E}_{s_t \sim P_t^{\pi_{\theta'}}} \mathbb{E}_{a_t \sim \pi_{\theta'}(\cdot |s_t)}[A^{\pi_\theta}(s_t, a_t)] \\
	&= \frac{1}{1-\gamma} \mathbb{E}_{s \sim \nu^{\pi_{\theta'}}} \mathbb{E}_{a \sim\pi_{\theta'}(\cdot |s)}[A^{\pi_\theta}(s, a)]
	\end{align}$$
	- 公式8到公式9用到了占度量的定义10，以及根据占用度量推导出的公式14，将所有时刻下期望的累加变成了用占用度量描述的随机变量的期望
	- 关于期望公式的写法$\mathbb{E}_{X \sim \rho} \mathbb{E}_{Y \sim \mu}[f(X,Y)]$和$\mathbb{E}_{X \sim \rho} [\mathbb{E}_{Y \sim \mu}[f(X,Y)]]$,两种写法是等价的,有时候为了简洁会采用前一种写法
	- 公式11中期望的展开式直接将$f(s_t)$变成了$f(s)$?(个人理解)
		- 公式11左边的含义是对每个时刻t求关于状态$s_t$的期望，展开就是对状态空间中的每个状态s乘上对应t时刻的状态分布概率再求和，应为状态空间和时刻无关所以这里也没必要标明是哪个时刻的状态空间，所以后边公式12中才可以使用占用度量$\nu_\pi(s)$替换$\sum_{t=0}^\infty \gamma^tp_t^\pi(s)$
		$$\begin{align}
		\nu^\pi(s) = (1 - \gamma) \sum_{t=0}^\infty \gamma^t P_t^\pi(s)
		\end{align}$$

$$\begin{align}
\sum_{t=0}^\infty \gamma^t \mathbb{E}_{s_t \sim P_t^\pi}[f(s_t)] &= \sum_{t=0}^\infty \gamma^t \sum_{s \in S} P_t^\pi(s)f(s)\\
&= \sum_{s \in S} \sum_{t=0}^\infty \gamma^tp_t^\pi(s)f(s)\\
&= \frac{1}{1-\gamma} \sum_{s \in S} \nu^\pi(s)f(s) \\
&=\frac{1}{1 - \gamma} \mathbb{E}_{s \sim \nu^\pi}[f(s)] \\
\end{align}$$

- 只要能够找到新的策略$\theta'$能够使公式9$\geq 0$,就相当于找个一个更优的策略,判断一个新的策略$/theta'$是不是更优策略的时候,公式9中不好获取的部分是新策略的占用度量$\nu^{\pi_{\theta'}}$，因为占用度量是一个统计量，因此用旧策略的占用度量近似替代新策略的占用度量，这在策略变化比较小的情况下是合理的，新策略的优化目标如下
	
	$$\begin{align}
	\mathcal{J}(\theta') = \mathcal{J}(\theta) + \frac{1}{1-\gamma} \mathbb{E}_{s \sim \nu^{\pi_\theta}} \mathbb{E}_{a \sim \pi_{\theta'}(\cdot | s)}[A^{\pi_\theta}(s,a)]
	\end{align}$$
	
	- 重要性采样，
	$$\begin{align}
	\mathbb{E}_{X \sim p}[f(x)] &= \int_x p(x)f(x) \;dx \\
	&= \int_x q(x) \frac{p(x)}{q(x)} f(x) \; dx\\
	&= \mathbb{E}_{X \sim q}\left[\frac{p(x)}{q(x)} f(x)\right] \\
	&=  \mathbb{E}_{X \sim q}\left[g(x)\right] \:; g(x) = \frac{p(x)}{q(x)} f(x)
	\end{align}$$
	
	- 公式15结合公式18可以将新策略的目标函数统一成关于旧策略动作分布下的期望,目标函数可以整理为下式,这样做的好处是可以在旧策略采样的数据上评估新策略的价值，否则每有一个新策略都需要采样评估代价太高。

$$\begin{align}
\mathcal{L}_\theta(\theta') = \mathcal{J}(\theta) + \mathbb{E}_{s \sim \nu^{\pi_\theta}} \mathbb{E}_{a \sim \pi_\theta(\cdot | s)} \left[\frac{\pi_{\theta'}(a|s)}{\pi_{\theta}(a|s)}A^{\pi_\theta}(s,a)\right]
\end{align}$$

- 能够用旧策略的占用度量来近似替代新策略的占用度量是建立在两个策略非常接近的基础上的，所以上式存在约束条件，加入约束条件的整体优化公式为

$$\begin{align}
\max_{\theta'} \mathcal{L}_\theta(\theta') \;\; \text{s.t.} \: \mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}}[D_{KL}(\pi_{\theta_k}(\cdot|s), \pi_{\theta'}(\cdot | s))] \leq \delta
\end{align}$$

- 上式中$\pi_{\theta_k}$表示k时刻的策略，和旧策略是一个意思只是换了个符号

## 近似求解
- 对目标函数采用一阶泰勒展开
$$\begin{align}
\mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}} \mathbb{E}_{a \sim \pi_{\theta_k}}(\cdot | s) \left[\frac{\pi_{\theta'}(a|s)}{\pi_{\theta}(a|s)}A^{\pi_\theta}(s,a)\right] \approx g^T(\theta' - \theta_k)
\end{align}$$
	- 其中g表示目标函数的梯度
$$\begin{align}
g = \nabla_{\theta'}\mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}} \mathbb{E}_{a \sim \pi_{\theta_k}}(\cdot | s) \left[\frac{\pi_{\theta'}(a|s)}{\pi_{\theta}(a|s)}A^{\pi_\theta}(s,a)\right]
\end{align}$$
	- 一阶泰勒展开的表达式为
$$\begin{align}
f(x) = \sum_{i=0}^n \frac{f^{(i)}(x_0)}{i!} (x - x_0)^i
\end{align}$$

- 约束条件在$\theta_k$处二阶展开如下式
$$\begin{align}
\mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}}[D_{KL}(\pi_{\theta_k}(\cdot|s), \pi_{\theta'}(\cdot | s))] \approx \frac{1}{2}(\theta' - \theta_k)^T H (\theta' - \theta_k)
\end{align}$$
- $H$表示策略之间平均KL距离的海森矩阵
$$\begin{align}
H = \mathcal{H}[\mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}}[D_{KL}(\pi_{\theta_k}(\cdot | s), \pi_{\theta'}(\cdot | s))]]
\end{align}$$

## 目标函数的一阶泰勒展开
- 为什么目标函数在$\theta_k$ 处的一阶泰勒展开没有函数的零阶导数项？
    - 将变量$\theta' = \theta_k$代入目标函数
    $$\begin{align}
    \mathcal{J}(\theta)_{\theta' = \theta_k} &= 
    \mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}} \mathbb{E}_{a \sim \pi_{\theta_k}(\cdot | s)} \left[\frac{\pi_{\theta_k}(a | s)}{\pi_{\theta_k}(a | s)} A^{\pi_{\theta_k}}(s,a)\right] \\
    &= \mathbb{E}_{s \sim \nu^{\pi_{\theta_k}}} \mathbb{E}_{a \sim \pi_{\theta_k}(\cdot | s)} \left[A^{\pi_{\theta_k}}(s,a)\right]
    \end{align}$$
    - 单独看后边这个期望，代入优势函数的定义$A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$
    $$\begin{align}
    \mathbb{E}_{a \sim \pi_{\theta_k}(\cdot | s)} A^{\pi_{\theta_k}}(s,a) &= \mathbb{E}_{a \sim \pi_{\theta_k}(\cdot | s)}[Q^\pi(s,a) - V^\pi(s)] \\
    &= \mathbb{E}_{a \sim \pi_{\theta_k}(\cdot | s)}[Q^\pi(s,a)] - V^\pi(s) \\
    &= V^\pi(s) - V^\pi(s) = 0
    \end{align}$$
    - 后边这个期望为0，所以期望整体为0，因此在$\theta_k$处的一阶泰勒展开没有函数的零阶导数项

## 约束条件的二阶泰勒展开
- 同样的约束条件的泰勒展开只剩下了二阶导数项
    - KL散度的公式为
    $$\begin{align}
    D_{KL}(\pi_\theta || \pi_{\theta'}) = \sum_a \pi_\theta(a|s) \log \frac{\pi_\theta(a|s)}{\pi_{\theta'}(a|s)}
    \end{align}$$
    - 首先零阶导数项是分布$\pi_{\theta_k}$和自己本身的距离，显然是0
    - 因为KL散度在$\theta' = \theta_k$处是个极小值，因此一阶导数也为0

# 目标函数的解析解形式
- 根据目标函数和约束条件的泰勒展开近似构建拉格朗日函数, 令$(\theta' - {\theta_k}) = x$
$$\begin{align}
\mathcal{L}(x, \lambda) = g^Tx - \lambda(\frac{1}{2}x^T H x - \delta)
\end{align}$$

- 对x求导并令导函数为零
$$\begin{align}
\nabla_x \mathcal{L}(x, \lambda) = g - \lambda H x = 0 \rightarrow x = \frac{1}{\lambda}H^{-1}g
\end{align}$$

- 将x代入约束项，通过约束项求$\lambda$, 这里通常$H^{-1}$为对称矩阵，因此$(H^{-1})^T = H^{-1}$
$$\begin{align}
\frac{1}{2} \left(\frac{1}{\lambda} H^{-1} g\right)^T H \left(\frac{1}{\lambda}H^{-1}g\right) = \frac{1}{2 \lambda^2} g^T H^{-1}g = \delta
\end{align}$$

- 整理得到
$$\begin{align}
\lambda = \sqrt{\frac{g^T H^{-1}g}{2 \delta}}
\end{align}$$

- 将求解的$\lambda$代入，因为想要优化的是参数$\theta'$，这里求解的是x，所以要换元回来
$$\begin{align}
\theta' &= \theta_k + x \\
&= \theta_k + \sqrt{\frac{2 \delta}{g^T H^{-1}g}} H^{-1}g
\end{align}$$
- 这里面对的是一个不等式约束的最优化问题，即新旧策略之间的KL散度小于等于一定的阈值$\delta$，但是上述过程直接当做等式约束处理的，chat老师说可以严格证最优点一定会撞到KL球的边界，我理解的是只要$\delta$设置的足够小，那么在这个信任区域内近似函数是单调的，所以最优解在信任区域的边缘。因此也就可以当做等式约束去处理

## 共轭梯度
- 以上$\theta'$的解析解形式中, g是策略的梯度, H是策略的协方差矩阵, $\delta$是超参数这些都是已知项, 但是问题是这里需要计算H矩阵的逆矩阵, 对于一个10000参数的策略模型来说, H矩阵的维度为10000x10000, 这个矩阵一般不能直接存储或者是计算逆矩阵, 因此解决方法是令$x = H^{-1}g$, 此时的更新公式变为
$$\begin{align}
\theta_{k+1} = \theta_k + \sqrt{\frac{2\delta}{x^T H x}} x
\end{align}$$
- 这里式子中唯一的未知量是x, 所以此时变成了$Hx=g$的求解问题, H是正定矩阵, 使用共轭梯度法求解.

## 广义优势估计

- 广义优势估计(Generalized Advantage Estimation，GAE), 是用来估计优势函数的, 时序差分误差表示为$\delta_t = r_t + \gamma(V(S_{t+1}) - V(S_t))$, V表示状态价值函数, 在TRPO中是价值函数给出的, 可以当做一个已知量, 根据多步时序差分的展开结果有
$$\begin{align}
A_t^{(1)} &= \delta_t = -V(S_t) + r_t + \gamma V(S_{t+1}) \\
A_t^{(2)} &= -V(S_t) + r_t + \gamma r_{t+1} + \gamma^2 V(S_{t+1}) \\
&= -V(S_t) + r_t + \gamma V(S_{t+1}) - \gamma V(S_{t+1}) + \gamma r_{t+1} + \gamma^2 V(S_{t+1}) \\
&= -V(S_t) + r_t + \gamma V(S_{t+1}) + \gamma \left[-V(S_{t+1}) + r_{t+1} + \gamma V(S_{t+1}) \right] \\
&= \delta_t + \gamma \delta_{t+1}
\end{align}$$

- 以此类推有步数为k的时序差分误差为:
$$\begin{align}
A_t^{(k)} = \sum_{l=0}^{k-1} \gamma^l \delta_{t+l}
\end{align}$$

- 常见的估计优势函数的方法如下, TRPO中采用了一种折中的方法, 使用指数移动平均对不同时刻的时序差分误差加权, 这种方法通常更加稳定
	1. 使用单步时序差分误差估计, 这种方法方差低但是偏差大
	2. 使用蒙特卡洛方法估计, 高方差低偏差

- 指数移动平均结果如下:
$$\begin{align}
A_t^{GAE} &= (1 - \lambda)(A_t^{(1)} + \lambda A_t^{(2)} + \lambda^2 A_t^{(3)} + ...) \\
&= \sum_{l=0}^{\infty}(\lambda\gamma)^l \delta_{t+l}
\end{align}$$
- [上述推导过程详见这里](https://hrl.boyuai.com/chapter/2/trpo%E7%AE%97%E6%B3%95#116-%E5%B9%BF%E4%B9%89%E4%BC%98%E5%8A%BF%E4%BC%B0%E8%AE%A1)

