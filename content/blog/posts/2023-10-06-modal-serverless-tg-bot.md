---
title: 把Serverless TG机器人架构模块化。
author: xiaowenz
type: post
date: 2023-10-06T06:00:00+08:00
slug: modal-serverless-tg-bot
description: "我花了一天的时间（感谢阿姨国庆节提前上班，让我能有一天完整的时间写自己的东西），把架构调整成了如下图所示……"
draft: false
categories:
  - I am a Developer
tags:
  - Telegram
  - Cloudflare
  - 技术
  - 微服务
---

![image.png](https://vip2.loli.io/2023/10/06/GWEKRDg8BptHA3L.png)

## 前情提要

[前文](https://xiaowenz.com/blog/2023/09/serverless-telegram-bot/)提到，我基于Cloudflare 的 Worker 搭建了一个无服务器(Serverless)的 Telegram 机器人，实现了一些自己想用的基础功能。

架构大概如下：

![image.png](https://vip2.loli.io/2023/09/21/kbvYLw5Oh1lFnAs.png)

之后，因为 CF 发布了边缘 AI 的支持能力，于是基于测试的目的，我在此架构上增加了一个翻译模块。[文章在这里](https://xiaowenz.com/blog/2023/09/serverless-ai/)

这个时候，很自然的，一个常见的架构问题出现了：

> 如果我希望继续增加新的场景，是继续构建新的代码并且嵌入到一起吗？

## 架构演进

我花了一天的时间（感谢阿姨国庆节提前上班，让我能有一天完整的时间写自己的东西），把架构调整成了如下图所示。

![image.png](https://vip2.loli.io/2023/10/06/l31ihTtwCMruSJ5.png)

如图，整个工程上从一个全能服务，调整成了1个网关服务 + N个独立功能性服务。

**这样做的好处显而易见：**

- Gateway 服务负责和 TG 的互动和请求的转发，只有通用功能。
- 其他服务只负责纯粹的业务功能，并根据实现方式独立绑定需要的资源，可以独立发布，升级。
  - 如：Translator 绑定了 CF 的 AI 资源；Counter 绑定了 CF 的 D1 数据库。
- 只有Gateway服务需要打开 Route 的互联网接入，其他服务关闭对外的接口，只允许网关服务以绑定资源的形式访问。
- 如果需要，在 Gateway 这一级可以平行的扩展出其他的渠道，比如 Discord 的机器人，邮件接入，或者微信机器人等，而后端服务可以完全复用。

**一些技术性细节如下：**

后端功能服务关闭对外的 HTTP 路由，只允许内部访问。

![功能服务关闭路由的配置](https://vip2.loli.io/2023/10/06/QFpiawsVZ1oeT2O.png)

后端服务只允许内部以绑定的形式访问。

![被 Gateway 服务绑定](https://vip2.loli.io/2023/10/06/ixqOhVErIwz6QbN.png)

Cloudflare 对于绑定服务通信的一些解释——没有网络延迟。你的微服务之间会像在同一个程序内交互一样快速。

![image.png](https://vip2.loli.io/2023/10/06/vfRT1xjG7Y8aXPW.png)

## 变成了这样

于是，现在的交互变成了这样。

![image.png](https://vip2.loli.io/2023/10/06/PAq2KCF8iaYXIvw.png)

通过在机器人的菜单里选择对应的功能，切换交互场景。

![image.png](https://vip2.loli.io/2023/10/06/kzolZXPJ7NRuMQA.png)

## 代码在哪里

- 网关：https://github.com/iamshaynez/telegram-assistant
- 翻译服务：https://github.com/iamshaynez/telegram-assistant-translator
- 打卡服务：https://github.com/iamshaynez/telegram-assistant-counter

## 之后可以干啥

之后，意味着可以随时增加有趣的功能，集成到同一个 Bot 里。我的个人预算和记账解决方案总算又着落了……

## 最后

很啰嗦，感谢你读完。