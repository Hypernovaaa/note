# 参考资料
- [论文地址](https://arxiv.org/pdf/2309.06180)
- [B站视频](https://www.bilibili.com/video/BV1kx4y1x7bu/?spm_id_from=333.337.search-card.all.click&vd_source=3ef5f4ed0881ee4ffcdfc06152c02352)
- [zh分页机制](https://zhuanlan.zhihu.com/p/352188978)

# 整体概述
- PagedAttention是通过高效利用现存, 避免现存浪费, 达到提升LLm模型推理吞吐量的效果
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.4joflcgkin.jpg" width=500>

- 以A100为例, 推理一个13B的模型, KV Cache占现存比例在30%以上, 随着batch size增大, 传统的大模型推理服务显存占用迅速上升, vllm则是有一个相对平缓很多的显存上升曲线, 同样显存占用下的每秒钟tokens吞吐量是传统方式的大概3倍

<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.67xsijvlaz.jpg" width=500>

- 从这里可以看出vllm提升内存使用效率的方式, 主要是通过减少保留内存和内存碎片的占用, 具体做法是受操作系统中的虚拟内存和分页内存的启发, 将传统上必须连续存放的一条请求的 KV Cache 拆分为固定大小的逻辑块（KV Block）,再映射到实际的物理块上
- 产生这么多内存碎片的原因:
    - 输出长度不确定：大模型在推理时，生成的 token 数量只有在遇到 eos 标记后才会确定。为了防止溢出，通常需要为 KV cache 预留一段足够大的显存空间。但如果实际生成的 token 数少于预留值，多出来的空间就被浪费了。
    - 预留空间的延迟使用：即便最终生成的 token 数量正好填满了预留空间，在推理初期，大部分预留区域仍然处于闲置状态，实际并未被使用，也是一种浪费。
    - 连续内存的限制：KV cache 的分配需要一段连续的显存。当显存中剩余的碎片空间虽然总量足够，但单块小于 KV cache 的需求时，就无法满足分配，导致这些零散的内存被闲置。