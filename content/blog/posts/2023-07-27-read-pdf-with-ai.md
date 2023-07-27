---
title: 大模型快速阅读行业报告。
author: xiaowenz
type: post
date: 2023-07-27T06:00:00+08:00
slug: read-pdf-with-ai
description: ""
categories:
  - I am a Developer
tags:
  - 人工智能
  - 金融
  - 行业
  - 生产力
---

尝试用 AI 快速辅助阅读材料，并提取关键信息的两个例子。目前的大模型服务几乎都支持 pdf 等格式的上传，解析了。

注：Markdown 格式的大纲可以方便的导为脑图格式，让你更容易的进行后续的信息整理。

## 案例 1 - 行业报告

数据源：中国第三方支付行业研究报告2021年.pdf

> Prompt:
>
> 请总结报告中的内容大纲，最多分三级，并以 Markdown 的格式输出给我。大纲中需要报告关键内容，关键引用的数据等信息。

![screencapture-poe-2021.png](https://vip2.loli.io/2023/07/27/1s2XBWKOvPMu4L9.png)

脑图的例子：

![image.png](https://vip2.loli.io/2023/07/27/DtQFUqdLxB1rP4H.png)

## 案例 2 - 报告之间的解读和比较

> Prompt:
>
> 请阅读两份 2021 年度和 2022 年度支付体系运行情况的报告，比较 2022 年度相比 2021 年度发生的变化情况，归纳成大纲的格式，最多三级，以 Markdown 输出给我。每一个变化点，列出引用的关键的比较数据。

![screencapture-poe.png](https://vip2.loli.io/2023/07/27/SQkUFmxfMB8n1Rz.png)

脑图：

![image.png](https://vip2.loli.io/2023/07/27/EgXMrpa3Q6kSuhv.png)

## 案例 3 - 英文文献

目前最优秀的几个大模型，基本也都支持了多语言的能力，意味着英文的论文也是可以用类似的方式辅助阅读的。

> Prompt:
>
> 请总结论文中的信息，汇总成翻译成中文的大纲格式，最多分三级，并以 Markdown 的格式输出给我。大纲中需要报告关键内容，关键引用的数据等信息。

数据源：Scientists Perspectives on the Potential for Generative AI in their Fields.pdf

![image.png](https://vip2.loli.io/2023/07/27/9s8ZU1kVhWzH4JN.png)

## 最后

目前的人工智能拥有了相对来说海量的脑容量（100K Token 可以容纳完整的书籍，笔记，论文），因此从非结构化的语意生成结构化的归纳甚至通过链式思考，进一步进化为更明确的结论性的答案（如分级，分类）也成为了可能。

供参考。