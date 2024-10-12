---
title: Mermaid
draft: false
slug: "mermaid"
---

## 这个页面用来测试 Markdown 里的 HTML 嵌入图表

<div id="mermaid-container"></div>

<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    let mermaidConfig = {
      startOnLoad: false,
      securityLevel: 'loose'
    };
    
    mermaid.initialize(mermaidConfig);

    function renderMermaid(data) {
      const container = document.getElementById('mermaid-container');
      container.innerHTML = ''; // 清空容器
      
      // 创建一个新的 pre 元素来包含 Mermaid 代码
      const pre = document.createElement('pre');
      pre.className = 'mermaid';
      pre.textContent = data;
      container.appendChild(pre);
      
      // 使用 mermaid.run() 来重新渲染
      mermaid.run({
        querySelector: '.mermaid'
      }).catch(error => console.error('Mermaid rendering error:', error));
    }

    function fetchAndRenderMermaid() {
      fetch('https://xiaowenz.com/mermaid.txt')
        .then(response => response.text())
        .then(data => {
          renderMermaid(data);
        })
        .catch(error => console.error('Error fetching Mermaid data:', error));
    }

    // 初次加载时渲染
    fetchAndRenderMermaid();

    // 添加刷新按钮
    const refreshButton = document.createElement('button');
    refreshButton.textContent = 'Refresh Mermaid';
    refreshButton.onclick = fetchAndRenderMermaid;
    document.body.insertBefore(refreshButton, document.getElementById('mermaid-container'));
  });
</script>