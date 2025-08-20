# 参考资料
- [论文地址](https://arxiv.org/pdf/2309.06180)
- [B站视频](https://www.bilibili.com/video/BV1kx4y1x7bu/?spm_id_from=333.337.search-card.all.click&vd_source=3ef5f4ed0881ee4ffcdfc06152c02352)
- [zh分页机制](https://zhuanlan.zhihu.com/p/352188978)
- [runpod分页内存](https://www.runpod.io/blog/introduction-to-vllm-and-pagedattention)

# 整体概述
- PagedAttention是通过高效利用现存, 避免显存浪费, 达到提升LLm模型推理吞吐量的效果
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.4joflcgkin.jpg" width=500>

- 以A100为例, 推理一个13B的模型, KV Cache占现存比例在30%以上, 随着batch size增大, 传统的大模型推理服务显存占用迅速上升, vllm则是有一个相对平缓很多的显存上升曲线, 同样显存占用下的每秒钟tokens吞吐量是传统方式的大概3倍

<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.67xsijvlaz.jpg" width=500>

- 从这里可以看出vllm提升内存使用效率的方式, 主要是通过减少保留内存和内存碎片的占用, 具体做法是受操作系统中的虚拟内存和分页内存的启发, 将传统上必须连续存放的一条请求的 KV Cache 拆分为固定大小的逻辑块（KV Block）,再映射到实际的物理块上
- 产生这么多内存碎片的原因:
    - 输出长度不确定：大模型在推理时，生成的 token 数量只有在遇到 eos 标记后才会确定。为了防止溢出，通常需要为 KV cache 预留一段足够大的显存空间。但如果实际生成的 token 数少于预留值，多出来的空间就被浪费了。
    - 预留空间的延迟使用：即便最终生成的 token 数量正好填满了预留空间，在推理初期，大部分预留区域仍然处于闲置状态，实际并未被使用，也是一种浪费。
    - 连续内存的限制：KV cache 的分配需要一段连续的显存。当显存中剩余的碎片空间虽然总量足够，但单块小于 KV cache 的需求时，就无法满足分配，导致这些零散的内存被闲置。
# pagedattention实现
## 连续内存模型
- 内存的低位地址用来存放操作系统, 一开始没有进程的时候内存状态如下:
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.58hp6cstv1.jpg" width=800>

- 随着不断拉起进程, 连续分配内存的情况下, 内存占用变成了:
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.6t7g5tq942.jpg" width=800>

- 当有进程退出的情况下, 内存占用:
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.4jofmc5oc8.jpg" width=800>

- 随着有进程退出内存中出现了大大小小的空洞, 如果这时候想要再起一个进程, 有可能会出现剩余内存总量足够但是没有一片连续内存能够放下这个新进程的情况, 这就是连续内存模型容易出现的外部碎片（External Fragmentation）, 显存中也是同样的道理, 在pagedattention出现之前就是使用的连续内存模型, 造成了大量的显存浪费

## 分页内存模型
- 分页内存的核心思想是主动把内存分割成固定大小的框, 把进程的逻辑地址空间分割成大小固定的页, 框和页的大小是相同的, 通过页表(page tabel)建立进程的逻辑内存地址到物理内存地址的映射, 这样从进程的角度来看它访问的内存是连续的, 分页内存模型的缺点是从逻辑地址到物理地址的转换增加了额外的寻址开销, 当没有占满一个page的情况下浪费的这部分内存称为内部碎片(internal fragmentation), 当然内部碎片要比外部碎片小得多
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250819/image.13m3u9ozhw.jpg" width=800>

- 把操作系统的分页内存套用到显存的管理上也是同样的道理, 只不过vllm这里不叫page而是称为KV Block, 并且KB Block是可以在内存也可以在显存的, 这里具体的调度由vllm内部管理
<img src="https://jsd.cdn.zzko.cn/gh/Hypernovaaa/picx-images-hosting@master/20250820/image.3k8c973tuj.jpg" width=800>

- 


