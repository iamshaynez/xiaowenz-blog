---
title: Serverless AI？
author: xiaowenz
type: post
date: 2023-09-28T06:00:00+08:00
slug: serverless-ai
description: ""
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 人工智能
  - Cloudflare
  - 技术
  - 思考
---

![image.png](https://vip2.loli.io/2023/09/28/pSxgzjREYTmQ1Ma.png)

## Cloudflare 的更新

昨天，Cloudflare 更新了数篇博客，分别发布了Serverless的开源模型接口，和基于 Worker 和 Pages 的 AI 开发包。

![image.png](https://vip2.loli.io/2023/09/28/iDlMwIJsF8Vg1Z2.png)

链接：https://blog.cloudflare.com/workers-ai/

同时，更新了向量数据库，D1 关系型数据库的 Open Beta 等。事实上，Cloudflare 以极快的速度，表现出了极大的野心让 Serverless 的生态，基本上具备了构建完整的中型乃至大型应用的能力。

## 简单的开发和兼容

于是，很容易的，我给自己的 Telegram 机器人助手增加了翻译的能力。

```javascript
import { AI } from "./env.js";
import { Ai } from '@cloudflare/ai'

export async function translate(sentence, from = "chinese", to = "english") {
    const ai = new Ai(AI);
    const response = await ai.run('@cf/meta/m2m100-1.2b', {
        text: sentence,
        source_lang: from, // defaults to english
        target_lang: to 
      }
    );
    return response["translated_text"];
}
```

> Wrangler 需要升级到最新的3.10.0，否则不能绑定 AI 资源

毕竟是开源的模型，翻译效果和 ChatGPT 差了十条街。

![image.png](https://vip2.loli.io/2023/09/28/KCl1IVkjuAa2TO9.png)

当前有的模型也只有这些：

- Text generation (large language model): meta/llama-2-7b-chat-int8
- Automatic speech recognition (ASR): openai/whisper
- Translation: meta/m2m100-1.2
- Text classification: huggingface/distilbert-sst-2-int8
- Image classification: microsoft/resnet-50
- Embeddings: baai/bge-base-en-v1.5

## 为什么

Cloudflare 的全球网络，意味着同样的服务，你可以轻松的构建全球范围内更低延迟，更低成本的环境依赖。

当前的商用大模型，几乎都构建在中心化的数据中心里；当前的数据中心，也在拿出为人工智能企业服务的，GPU 算力的池的方案，用来缓解大功耗带来的潮汐现象，高成本问题。

Cloudflare 作为全球基础设施的基础设施，有更好的条件去摊平这些成本，提供真正的边缘 GPU 计算资源，并让人按需付费的使用。

## 等什么

等等吧，等 Cloudflare 提供 Serverless 的模型部署，更多模型的接入，甚至是 Fine-tune 的 Serverless 方案。

小企业，就有了更低入局的门槛。

## 最后

很啰嗦，感谢你读完。

我真实喜欢 Cloudflare 啊……

