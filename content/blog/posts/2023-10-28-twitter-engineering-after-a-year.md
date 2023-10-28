---
title: 一篇精彩的推文，一年后的推特工程实践。
author: xiaowenz
type: post
date: 2023-10-28T06:00:00+08:00
slug: twitter-engineering-after-a-year
description: "你的快乐，悲伤，成功或困境，在自己的家里才是最真切的。属于自己的枕头和床，永远是最柔软安全的栖息地。"
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 技术
  - 思考
  - 工程
  - 推特
---

![image.png](https://vip2.loli.io/2023/10/28/UygXHTBsdnVo7bL.png)

## 马斯克的一周年。

昨天是2023年10月27日，马斯克入主推特一周年。推特官方和关联账号，发布了若干这一周年从第一视角，企业发生的变化。之前我写过一篇《Twitter 要去哪里。》，站在当时充满质疑的一系列操作的进行时中，试图思考从商业上，这家企业究竟在做什么。

如今，已经更名为 X 的这家企业，工程技术部门也发了一篇长推，总结了这波澜壮阔的一年里，从工程师的视角，究竟发生了些什么。

![image.png](https://vip2.loli.io/2023/10/28/wKgP4DFmXn8Wxus.png)

非常有意思，值得一读。

## 全文如下，配上我的逐段备注解读。

This has been a year full of engineering excellence that sometimes can go unnoticed. Besides all the visible changes you see on our app, here are some of the most important improvements we have made under the hood.

这是一个充满也许会被忽视的卓越工程实践的一年。除了你在我们的应用中肉眼可见的功能性改变，这里是我们在幕后做出的一些最重要的改进。

> Comment：是的，非功能和功能，同样重要。

- Consolidated the tech stacks for For you, Following, Search, Profiles, Lists, Communities and Explore around a singular product framework.

- 我们整合了“为你”、“关注”、“搜索”、“个人资料”、“列表”、“社区”和“探索”等功能背后的技术架构，整个产品统一了内部框架。

> Comment：软件研发出生的朋友，更能理解这意味着什么——更容易维护的软件架构，显著降低的未来研发成本，更低的不确定性。

- Completely rebuilt the For you serving and ranking systems from the ground up, resulting in a decrease 90% reduction in lines of code from 700K to 70K, a 50% decrease in our compute footprint, and an 80% increase in the throughput of posts scored per request.

- 我们从头开始完全重建了"为你"的服务和排名推荐系统，结果代码行数从700K减少到70K，减少了90%，我们的计算足迹减少了50%，吞吐量增加了80%。

> Comment: 90%的冗余代码，这可能吗？如果一个系统维护了几十年，那必然是可能的。但如此大规模的重构（所带来的风险），对工程师来说，也许只是个梦境。很高兴在 X，这件事实现了。

- Unified the For you and video personalization and ranking models, which significantly improved video recommendation quality.

- 我们统一了"为你"和视频个性化和排名模型，这大大提高了视频推荐的质量。

> Comment: 虽然我并不会在推特看视频，我不看任何短视频。

- Refactored the API middleware layer of our tech stack and in doing so simplified the architecture by  removing more than 100K lines of code and thousands of unused internal endpoints and eliminating unadopted client services.

- 我们重构了我们技术堆栈的API中间件层，通过移除超过100K行的代码和数千个未使用的内部端点，以及消除未被采纳的客户端服务，从而简化了架构。

> Comment: 不知道为什么，这样的描述让我这个局外人，由衷的感觉到快乐。

- Reduced post metadata sourcing latency by 50%, and global API timeout errors by 90%.

- 我们把帖子元数据的获取延迟降低了50%，全球API超时错误降低了90%。

> Comment: 发帖子确实感觉顺畅一些了，其他倒是感觉不深。

- Blocked bots and content scrapers at a rate +37% greater than 2022. On average, we prevent more than 1M bots signup attacks each day and we’ve reduced DM spam by 95%.

- 我们以比2022年高37%的速度阻止了机器人和内容抓取器。平均每天，我们阻止超过1M个机器人注册攻击，我们已经把DM垃圾邮件降低了95%。

> Comment: 我一直认为，马斯克上任的第一件事，就是挤掉职业经理人经营多年的水份。机器人和自动化垃圾营销内容，显然是大头。

- Shutdown the Sacramento data center and re-provisioned the 5,200 racks and 148,000 servers, which generated more than $100M in annual savings. In total, we freed up 48 MW of capacity and tore down 60k lbs. of network ladder rack before re-provisioning it to other data centers.

- 我们关闭了萨克拉门托数据中心，并重新配置了5,200个机架和148,000个服务器，这为我们每年节省了超过1亿美元。总的来说，我们释放了48 MW的容量，并拆除了60k磅的网络梯子，然后将它重新配置到其他数据中心。

> Comment: 如果你感兴趣，可以去读读马老板自己开车冲到数据中心拔网线的故事。非常有趣的体验。

- Optimized our usage of cloud service providers and began doing much more on-prem. This shift has reduced our monthly cloud costs by 60%. Among the changes we made was a shift of all media/blob artifacts out of the cloud, which reduced our overall cloud data storage size by 60%, and separately, we succeeded in reducing cloud data processing costs by 75%.

- 我们优化了我们对云服务提供商的使用，并开始在本地做更多的事情。这个转变使我们每月的云成本减少了60%。我们做出的改变中，有一个是把所有的媒体/blob工件从云中移出，这使我们的整体云数据存储大小减少了60%，另外，我们成功地把云数据处理成本降低了75%。

> Comment: 多年来，我始终坚定的认为，云对于成本的影响是要精细化来看的，不能一概而论。不同于算力的弹性伸缩，大部分时候，系统的存储是线性而非弹性的。算力上云，意味着不为闲置的谷底埋单，但存储上云，除了数据容灾少一些工程成本外，整体上是昂贵的。
>
> 「媒体/blob」从云上拿出来，显然是把推特的存储部分，回归了自己的数据中心内。
>
> 结合 37signals 创始人 @DHH 这几年大张旗鼓的规模化去云服务的论调，从技术决策的角度其实越来越清晰了：云服务的经济性和企业规模成反比，虽然临界值并不容易测算，但精细化的算算账，不是难事。

- Built on-prem GPU Supercompute clusters and designed, developed, and delivered 43.2Tbps of new network fabric architecture to support the clusters.

- 我们在本地建立了GPU超级计算集群，设计、开发并交付了43.2Tbps的新网络布局架构来支持这些集群。

> Comment: 算力的天下，推特迟早会踏上这条大船的。

- Scaled network backbone capacity and redundancy, which resulted in $13.9M/year in savings.

- 我们扩大了网络骨干的容量和冗余，这为我们每年节省了1390万美元。

> Comment: 网络的规划和成本测算，也是需要跟随应用规模不断观测和调整的。

- Started automated peak traffic failover tests to validate the scalability and availability of the entire platform continuously.

- 我们开始进行自动化的高峰流量故障切换测试，以持续验证整个平台的可扩展性和可用性。

> Comment: 哈？以前不是吗？

## 所以呢？

所以，这意味着推特的工程团队，投入了巨大的成本承担了巨大的风险，进行了几乎「伤筋动骨」的重构。这一年里，虽然平台也出过些小问题，但看起来，大部分的重构已经完成，推特最终实现了风险可控的大规模改造，为以后的轻装上阵铺平了路。

## 非功能性的成本和收益。

应用系统的非功能性，对业务部门不可见，对用户也不可见，但是对于软件本身的可维护性，健壮度，至关重要。

但换句话说，这意味着只有技术人员更能看明白其价值，非技术背景的相关方，很容易被**忽悠**。

这也就是为什么，在很多企业里，工程师们坚持长期的维护**屎山**，却无法立一个项目来给存量填填坑————重构的成本高，风险大，但收益难以度量————这个项目存在风险，批准这样的项目，往往才是最大的风险。

## 所以呢？

所以，需要的是一个懂技术，有意愿承担风险，有能力承担成本的老板。

大概这样规模的工程投入，这世界上只有推特能做到了。

## 最后。

虽不能至，心向往之，替推特的工程师们高兴。

## 最后的最后。

感谢你读完。

