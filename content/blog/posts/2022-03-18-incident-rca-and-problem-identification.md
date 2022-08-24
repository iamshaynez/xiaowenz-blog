---
title: Incident RCA and Problem Identification
author: xiaowenz
type: post
date: 2022-03-18T08:40:24+00:00
url: /2022/03/18/276.html
categories:
  - I am a Developer
tags:
  - ITIL
  - ITSM
  - 工作
  - 方法论
  - 管理

---
<blockquote class="wp-block-quote">
  <p>
    本指引用来描述一般意义的由生产事故作为入口的根因分析和问题管理方法。
  </p>
</blockquote>

### **背景**

  * 事故定义应着眼于服务不可用而非系统技术性故障，否则广义范围的问题管理方法则不适用。
  * 问题管理制度应允许事故导向多个问题单，并分别定级和推进。

### **问题管理原则**

问题管理的最终目标，是提高服务的业务可用性（Availability）。服务可用性以生产事故（Incident）的产生而中断，已生产事故的修复而恢复。服务可用性的提高，大多数时候表现为：

（三个固定问题）

  * 找到事故的技术根因
  * 使生产事故（Incident）发生的概率减少
  * 若生产事故不可避免，使生产事故发生后的修复时间缩短

### **MTTR及相关定义**

  * MTTR（Mean Time To Repair，平均修复时间）源自于IEC 61508中的平均维护时间（Mean Time To Repair），目的是为了清楚界定术语中的时间的概念，MTTR是随机变量恢复时间得期望值。
  * MTTI（Identify），MTTK（Know），MTTF（Fix），MTTV（Verify）
  * MTBF（Between）

### **问题管理的常规方法论**

<blockquote class="wp-block-quote">
  <p>
    以MTBF的扩大为导向，分析事故的根因，制定规避方案
  </p>
  
  <p>
    以MTTR时间线为导向，分析事故的修复过程中的各个重要环节，识别低效率点，并制定改进方案
  </p>
  
  <p>
    建议：对每个改进面创建问题单，进行定级，分拣和后续推进
  </p>
</blockquote>

### **MTBF：通过修复根因，评估修复方案和改进点**

  * 必须：事故技术原因，修复——修复可能是技术补丁，升级，扩容等
  * 可选：质量控制环节的补足
  * 可选：容量规划环节的补足
  * 其他

### **MTTR：通过时间线分析，评估改进点**

  * MTTI：一般指事故实际发生的时间到事故被科技团队有效识别的时间，MTTI时间显著，可能意味着：
      * 监控能力的缺失或薄弱
      * 科技团队内部上升，信息传递制度存在缺陷
      * 业务团队事故上报的流程，上升路径存在缺陷
  * MTTK：一般指事故被科技团队（任何）知晓后，最终传递到正确的事故修复团队，并明确修复方案的时间。MTTK时间显著，可能意味着：
      * 监控能力的缺失或薄弱，导致最终根因的有效信息未能第一时间通过监控反应
          * 如：网络引起的应用系统性能下降，告警平台只能反映出系统问题，但网络相关告警未能展示网络性能下降
      * 科技团队内部上升，信息传递制度存在缺陷
      * 事故修复团队内部知识库缺失，导致根因分析效率低
      * 应用系统的日志缺失，可运维性较差，难以在不查阅代码的场景下排查事故
  * MTTF：一般指事故根因明确后，技术团队实施修复措施所消耗的时间，如重启，补丁发布，数据变更等；MTTF时间显著，可能意味着：
      * 技术团队知识库缺失，修复效率较低
      * 系统或组件可运维性较差，恢复方案复杂，或因性能导致恢复慢
  * MTTV：指技术团队实施修复后，能够明确确认服务已恢复的时间。确认服务恢复，可能是：业务确认，监控确认，科技手工验证等；MTTV时间显著，可能意味着：
      * 系统或组件可运维性较差，无有效手段（监控指标）度量服务可用性（Service Measurement）
      * 其他原因