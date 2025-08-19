@[TOC]
# Actor-Critic
- Actor-Critic是一类算法的总称，Q-learning和DQN只学习动作价值，REINFORCE只学习策略，Actor-Critic算法是两者的综合，本质上是基于策略的算法，但是会额外学习价值函数辅助策略学习。
- 策略梯度的一般形式如下
$$\begin{align}
g = \mathbb{E}\left[\sum_{t=0}^T \psi_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\right]
\end{align}$$
	- 上式中涉及价值计算的部分是$\psi_t$表示从t时刻执行动作$a_t$之后的回报，REINFORCE算法中使用的是采样玩整条序列之后的无偏估计，也就是真实值，这里要用模型直接估计$\psi_t$
## 价值模型的演化
- 为什么是这种形式（个人理解，总感觉这里不太对😒）
- 最直观的方式是直接定义一个模型输出当前动作的价值$Q^{\pi_\theta}(s_t, a_t)$，就像在DQN中做的一样，直接建模动作价值函数在这里其实是不够的，比如我们有个动作价值函数可以输出当前动作的价值是5，或者10这其实没有意义，我们想要的其实是当前的动作相比最优动作差多少，这个相对值才能评估当前动作的好坏，策略函数$\theta$才能够根据策略的好坏优化输出动作的分布
- 回顾Dueling DQN算法对价值模型的改进，不直接输出动作价值，而是输出动作价值的分解项，也就是状态价值$V(s)$和当前状态下执行动作a相对基准能够获得的增益也就是优势函数$A(s,a)$，这种分开建模的形式有助于模型捕捉“动作好坏”和“状态好坏”之间的区别，这里价值模型的作用是评估策略的好坏也就是动作好坏，动作好坏是用优势函数建模的，也就是说这里需要的其实是优势函数
$$\begin{align}
A^{\pi_\theta}(s_t,a_t) &= Q^{\pi_\theta}(s_t,a_t) - V^{\pi_\theta}(s_t) \\
&\approx r_t + \gamma V^{\pi_\theta}(s_{t+1}) - V^{\pi_\theta}(s_t)
\end{align}$$
	- 这里$r_t$是当前时刻的环境奖励，是个已知项，也就是说知道状态价值函数就可以推导出优势函数
	- 公式2叫做优势函数，公式3叫做时序差分残差，它们两者之间的区别是优势函数是一个精确值，时序差分残差是一个估计值
	- 公式3是价值模型的最终形式
## Critic模型损失函数
$$
\mathcal{L}(\omega) = \frac{1}{2}\left(r + \gamma V_\omega (s_{t+1}) - V_\omega(s_t)\right)^2
$$
- 上述公式中的$r + \gamma V_\omega (s_{t+1})$作为时序差分目标，类似Double DQN中的目标网络的输出，当做标签处理，可以理解为是个常量，因此价值函数的梯度为可以根据链式求导法则推理为下式
$$
\nabla_\omega \mathcal{L}(\omega) = -\left(r + \gamma V_\omega (s_{t+1}) - V_\omega(s_t) \right) \nabla_\omega V_\omega(s_t)
$$
