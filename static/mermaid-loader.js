(function() {
    // 创建 Mermaid 容器
    var container = document.createElement('div');
    container.id = 'mermaid-container';
    document.body.appendChild(container);
  
    // 创建并添加 Mermaid 脚本
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js';
    script.onload = function() {
      // 配置 Mermaid，增加最大文本大小限制
      mermaid.initialize({ 
        startOnLoad: true,
        maxTextSize: 100000  // 增加最大文本大小限制，可以根据需要调整
      });
  
      // 从同域名下获取 Mermaid 数据
      fetch('/mermaid.txt')
        .then(function(response) { return response.text(); })
        .then(function(data) {
          container.className = 'mermaid';
          container.textContent = data;
          mermaid.init(undefined, container);
        })
        .catch(function(error) { console.error('Error fetching Mermaid data:', error); });
    };
    document.head.appendChild(script);
  })();