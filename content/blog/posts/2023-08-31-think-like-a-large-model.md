---
title: 学会像大模型一样思考。
author: xiaowenz
type: post
date: 2023-08-31T06:00:00+08:00
slug: think-like-a-large-model
description: ""
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 人工智能
  - 科技
  - 思考
  - 生产力
---

## 大模型的思考特征

目前，海量数据和知识训练出的大模型，只能依靠一次一次的响应式的 Chat 来和人交互，其每一次反馈，实际上都是神经网络分层结构对人类「输入」产生的「输出」而已。

- **反应式思考**：大模型的思考方式主要是反应式的，也就是说，它不会主动思考，而是根据输入信息进行响应。它没有自我意识，也没有主观意愿。
- **短期记忆**：由于模型的设计，大模型主要依赖于短期记忆。例如，GPT-3可以处理上下文长度为2048个令牌，这限制了其长期连贯的思考能力。
- **无状态**：大模型是无状态的，这意味着它们在每一次响应之后并不保留任何信息。每次的输入都是独立的，模型无法记住以前的信息。

所谓的上下文，实际上也不过是吧所有的信息平面化的输入模型中，一次次的再更大的上下文中获得输出，让人产生了「模型可以在很大的上下文中思考」的幻觉。

因此，即使是 ChatGPT4，对于复杂问题的理解和解决能力，也和人类有巨大的差距。

## 教会大模型思考

基于这样的现状，人们在和大模型交互的过程里，学会了如何教会大模型构件自己的思考路径，并在有限的上下文里，更有逻辑的解决复杂的问题。

### Chain Of Thought

文献：[Automatic Chain of thought Prompting in Large Language Models](https://arxiv.org/abs/2210.03493)

![image.png](https://vip2.loli.io/2023/08/31/QVCzXEMawUS6GR9.png)

![image.png](https://vip2.loli.io/2023/08/31/k4YtKnBDEpMdozG.png)

![image.png](https://vip2.loli.io/2023/08/31/2VgqKIdybzE4wjf.png)

其核心在于，对于每一个采样的问题拼接上“Let's think step by step”（类似于 Zero-Shot-CoT ）输入到语言模型，让语言模型生成中间推理步骤和答案，然后把这些所有采样的问题以及语言模型生成的中间推理步骤和答案全部拼接在一起，构成少样本学习的样例，最后再拼接上需要求解的问题一起输入到语言模型中进行续写，最终模型续写出了中间的推理步骤以及答案。

### Least To Most Prompting

文献：

- [LEAST-TO-MOST PROMPTING ENABLES COMPLEX REASONING IN LARGE LANGUAGE MODELS](https://arxiv.org/abs/2205.10625)
- [Teach Language Models to Reason](http://dennyzhou.github.io/Teach-LLMs-to-Reason-KDD-2023.pdf)

作为 CoT 的加强版，其核心要义是，用多次调用，先让模型「只分解问题」，再「解决问题」。能获得更优的复杂问题的 Break Down 的效果，并在模型上下文中搞定最终的逻辑关系。

## 然而

如果我们把大模型面对复杂问题的时候，大部分时候返回不正确也不错误的车轱辘话，作为一种「你不能说他错，但确实也没解决任何问题」的行为特征，而运用上述的技巧，教会模型如何思考，作为一种「复杂问题逐步落地」的更优结果……

现实才是残酷的，你会惊讶的发现，许多人类，就像一个大模型一样，面对复杂问题，一样的只会说车轱辘话。

**面对长期的目标，面对千里外的美景，人们需要更多的学会找到「跬步」，一步一步不可逆的前进。**

> 就像你们教模型的那样，教会你们自己如何思考。

## 最后

每次都有最后，我来提供一个有趣的链式思考的 Prompt 的例子。

这个例子可以让模型像苏格拉底一样，不断的自我思考，反问，最终找到「生命的最终答案」。

```
Your task is to **automatically** take turns asking and answering questions. We’ll begin with an initial question. Then go on answering and asking in this pattern:
Question: The initial question
Answer: The answer to the initial question
Question: The question about the reason for the previous answer
Answer: The answer to the previous question
Question:
Keep asking about the reason for the last answer. Stop only when the answer is "That's the way it is" or "We don't know for now". Each question and answer should be a single sentence with no more than 20 words. Add "Q: " before each question and "A: " before each answer.
Ask and answer in "Chinese" regardless of the language I use. Don’t show the translation process. Just write questions and answers in the destination language.
Now, the initial question is: "Why the robots are all made the shape human-like"
---

The initial question is: "Why is the night sky dark?" Now, start asking and answering in terms of "astronomy".
```

上述这个例子的 ChatGPT4 的答案是：

```
Q: 为什么夜晚的天空是黑的？
A: 这是因为太空中的大部分地方没有光线照亮。

Q: 为什么太空中的大部分地方没有光线照亮？
A: 这是因为除了星星和其他天体发出的光线外，太空基本上是空的。

Q: 星星和其他天体发出的光线为什么不能照亮整个太空？
A: 这是因为宇宙是无限的，且光线会随着距离的增加而衰减。

Q: 为什么光线会随着距离的增加而衰减？
A: 这是因为光线在传播过程中会受到各种因素的影响，例如空间尘埃。

Q: 为什么空间尘埃会影响光线的传播？
A: 这是因为尘埃粒子可以散射和吸收光线，这会导致光线的衰减。

Q: 尘埃粒子是怎么散射和吸收光线的？
A: 这是因为光线与尘埃粒子相互作用时，能量会被转移或者吸收。

Q: 光线与尘埃粒子相互作用的具体过程是什么？
A: 这个问题目前还没有确切的答案，科学家们正在进行相关的研究。
```

同样的例子中，Claude2 的答案：

```
Q: 为什么夜空是黑的?
A: 因为在夜晚,太阳在地球的另一边,所以夜空没有太阳的光照亮。
Q: 夜晚为什么看不到太阳?  
A: 因为地球自转,使得太阳定期出现和消失在地平线以上。
Q: 地球为什么会自转?
A: 这是地球的一个基本运动特性,源于它形成时的角动量。
Q: 为什么地球形成时有角动量?
A: 这是行星形成过程中的一个普遍特征,可能源于原始星云的自转运动。
Q: 原始星云的自转从何而来?
A: 这可能是大爆炸后残余气体的混乱运动形成的。
Q: 为什么会有大爆炸?
A: 关于宇宙的起源,目前我们还不完全明了,需要进一步的科学研究。
```

希望你喜欢，希望你喜欢思考。