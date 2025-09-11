## llm中用到的Norm

### RMSNorm 均方根标准化
$$\begin{align}
RMSNorm(x) = \frac{x}{\sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}} * \gamma 
\end{align}$$


### LayerNorm & BatchNorm 
$$\begin{align}
LayerNorm(x) &= \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \gamma + \beta \\
\mu &= \frac{1}{d} \sum_{i=1}^d x_i \\
\sigma^2 &= \frac{1}{d} \sum_{i=1}^d (x_i - \mu)^2 
\end{align}$$