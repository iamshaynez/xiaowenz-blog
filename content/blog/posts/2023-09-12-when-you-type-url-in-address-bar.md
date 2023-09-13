---
title: 把老问题想清楚：浏览器里输入地址按下回车后，发生了什么。
author: xiaowenz
type: post
date: 2023-09-12T06:00:00+08:00
slug: when-you-type-url-in-address-bar
description: ""
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 技术
  - 学习
  - 知识
---

![p63stxq7xtmb1.gif](https://vip2.loli.io/2023/09/12/DkBfOITcVXF76RZ.gif)

## 说起来都会，用起来懵逼

这是一道传统的面试题，属于说了每个人都会的那种车轮子题。

很多技术知识就是这样，说起来都知道，用起来就懵逼。技术人和技术人的差距，大抵上就在这里了。

我的建议是：不要做这种人。

所以，在浏览器里输入了地址以后，事实上发生的事儿大概有这么几个：

- DNS
- TCP
- SSL/TLS
- HTTP

这些细节，其实都很有意思的。

## 关于 DNS

DNS说起来也简单，毕竟谜底就在谜面上，解析域名的嘛。大部分工程师都知道 DNS 就是把域名转换为 IP 地址的过程，但接下来，以下两个问题你是否有答案？

> 如果 nslookup 可以返回结果，但 ping 的时候 host 不存在，可能的原因是什么？

> 网传，localhost 不经过网卡，127.0.0.1 经过网卡，是真的吗？所以 localhost 比 127.0.0.1 性能上更快，是对的吗？

如果你并没有直接的答案，也没有验证这些结论的思路，那么大概率的，你对这部分的知识还停留在「看了就是懂了」的程度。进一步去看看，进一步动动手，如何？

推荐几篇笔记文章：

~~~
Linux 系统如何处理名称解析

https://blog.arstercz.com/linux-%E7%B3%BB%E7%BB%9F%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E5%90%8D%E7%A7%B0%E8%A7%A3%E6%9E%90/

Anatomy of a Linux DNS Lookup

https://zwischenzugs.com/2018/06/08/anatomy-of-a-linux-dns-lookup-part-i/


就是要你懂DNS--一文搞懂域名解析相关问题

https://plantegg.github.io/2019/06/09/%E4%B8%80%E6%96%87%E6%90%9E%E6%87%82%E5%9F%9F%E5%90%8D%E8%A7%A3%E6%9E%90%E7%9B%B8%E5%85%B3%E9%97%AE%E9%A2%98/
~~~

## 关于 TCP

实际上，作为 HTTP 的底层，TCP 上消耗的成本远比你想想的要多。

如果除了「三次握手」之外，你就不太清楚了，Linux 上如何处理 TCP，从握手的队列，到传输和缓存的窗口，客户服务端之间的网络是如何放大 TCP 性能的，这些更细节一些的问题如果你没有具体的思路去验证，下面这些文章是适合你进一步去了解的。

~~~
就是要你懂 TCP

https://plantegg.github.io/2018/06/14/%E5%B0%B1%E6%98%AF%E8%A6%81%E4%BD%A0%E6%87%82TCP--%E6%9C%80%E7%BB%8F%E5%85%B8%E7%9A%84TCP%E6%80%A7%E8%83%BD%E9%97%AE%E9%A2%98/

从一次线上问题说起，详解 TCP 半连接队列、全连接队列

https://www.51cto.com/article/687595.html

以及一个动手实验，见下图：
~~~

![image.png](https://vip2.loli.io/2023/09/13/5OlDNHGIxsbiTYn.png)

## SSL/TLS

关于证书。

说起来，都知道这玩意是保障安全的，是用来加密的。但现实中我却发现，因为知其然不知其所以然，很多人在设计应用的安全部分的时候，几乎是本末倒置的。

- 一味的设计加密链路，但对密钥的保护却非常草率
- 没有系统性的理解 TLS 握手的原理，遇到问题，一味的选择 no-verify

这里就推荐一篇，我很喜欢的一位 SRE 的文章。

~~~
有关 TLS/SSL 证书的一切

https://www.kawabangga.com/posts/5330

HTTPS 的实践

https://blog.laisky.com/p/https-in-action/
~~~

## HTTP

实际上，标准的 HTTP 是有一套「语言」的。但由于国内的奇怪的历史原因，无论是 HTTP Code，还是 Method，大部分国内的实践都有些简单粗暴……

对于应用层最可见的一层协议，一些基本的知识还是应该知道的更完整一些的。

值得注意的是，未来的 HTTP（虽然也许很遥远）并不会基于 TCP 了。

~~~
关于 HTTP

https://blog.csdn.net/zjbyough/article/details/113898780
~~~

## 最后

这不是一篇技术性科普文章，更多的是串一下自己之前阅读和收集的笔记。技术这种事，有就是有，没有就是没有，我是真的不喜欢知其然不知其所以然的感觉。

因为要发微信，所以超链接采用了很挫的形式。
