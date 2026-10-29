/**
 * 玄墨 · comments.js
 * 评论区：GET {coreAPI}/api/comments?post=slug 渲染列表；
 * 提交表单 POST {coreAPI}/api/comments（字段 post/name/email/content/蜜罐 website/turnstile_token）。
 * 无 JS 时整个 section 保持 hidden。
 */
(function () {
  "use strict";

  function coreAPI() {
    return (window.XW && window.XW.coreAPI) || "";
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fmtDate(s) {
    var d = new Date(s);
    if (isNaN(d.getTime())) return s || "";
    function p(n) { return (n < 10 ? "0" : "") + n; }
    return d.getFullYear() + "." + p(d.getMonth() + 1) + "." + p(d.getDate());
  }

  function renderList(comments) {
    if (!comments || !comments.length) {
      return '<p class="xw-comment-empty">还没有评论，来抢沙发。</p>';
    }
    var html = '<ul class="xw-comment-list">';
    comments.forEach(function (c) {
      html +=
        '<li class="xw-comment">' +
        '<div class="xw-comment__meta">' +
        '<span class="xw-comment__name">' + esc(c.author_name || c.name || "匿名") + "</span>" +
        "<span>" + esc(fmtDate(c.created_at || c.date || c.createdAt)) + "</span>" +
        "</div>" +
        '<div class="xw-comment__content"><p>' + esc(c.content || "").replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br>") + "</p></div>" +
        "</li>";
    });
    return html + "</ul>";
  }

  function turnstileSiteKey() {
    return (window.XW && window.XW.turnstileSiteKey) || "";
  }

  function renderForm(slug) {
    var ts = turnstileSiteKey()
      ? '<div class="cf-turnstile" data-sitekey="' + esc(turnstileSiteKey()) + '"></div>'
      : "";
    return (
      '<form class="xw-comment-form" method="post" action="' + coreAPI() + '/api/comments">' +
      '<input type="hidden" name="post" value="' + esc(slug) + '">' +
      '<input name="name" placeholder="名字" required>' +
      '<input name="email" type="email" placeholder="邮箱（选填，不公开）">' +
      '<textarea name="content" class="xw-field--full" placeholder="写下你的评论…" required></textarea>' +
      '<input name="website" type="text" class="xw-hp" value="" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      ts +
      '<button type="submit">提交评论</button>' +
      '<p class="xw-form-status xw-field--full" role="status" aria-live="polite" hidden></p>' +
      "</form>"
    );
  }

  // Turnstile api.js 是 async 加载的：就绪前轮询，就绪后渲染容器里的 widget
  function mountTurnstile(form) {
    var container = form.querySelector(".cf-turnstile");
    if (!container || !window.turnstile) {
      if (container && !container.getAttribute("data-xw-ts")) {
        container.setAttribute("data-xw-ts", "1");
        var tries = 0;
        var timer = setInterval(function () {
          tries += 1;
          if (window.turnstile || tries > 50) { // 约 5s 后放弃（api.js 加载失败时表单仍可提交，由 core 拒绝）
            clearInterval(timer);
            if (window.turnstile) mountTurnstile(form);
          }
        }, 100);
      }
      return;
    }
    window.turnstile.render(container);
  }

  function init() {
    var section = document.querySelector("[data-xw-comments]");
    var box = document.getElementById("comments");
    if (!section || !box || !window.fetch) return;
    var slug = box.getAttribute("data-post");
    if (!slug) return;
    section.hidden = false;

    function load() {
      fetch(coreAPI() + "/api/comments?post=" + encodeURIComponent(slug), { headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        })
        .then(function (data) {
          var list = Array.isArray(data) ? data : (data && (data.comments || data.items || data.data)) || [];
          box.innerHTML = renderList(list) + renderForm(slug);
          bindForm();
        })
        .catch(function () {
          box.innerHTML = '<p class="xw-comment-empty">评论加载失败。</p>' + renderForm(slug);
          bindForm();
        });
    }

    function bindForm() {
      var form = box.querySelector(".xw-comment-form");
      if (!form) return;
      mountTurnstile(form);
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var status = form.querySelector(".xw-form-status");
        var btn = form.querySelector('button[type="submit"]');
        var payload = {
          post: slug,
          name: (form.elements.name.value || "").trim(),
          email: (form.elements.email.value || "").trim(),
          content: (form.elements.content.value || "").trim(),
          website: (form.elements.website.value || "").trim()
        };
        var ts = form.querySelector('[name="cf-turnstile-response"]');
        if (ts && ts.value) payload.turnstile_token = ts.value;
        if (!payload.name || !payload.content) {
          if (status) {
            status.hidden = false;
            status.textContent = "请填写名字和评论内容。";
            status.classList.add("is-err");
          }
          return;
        }
        if (btn) btn.disabled = true;
        fetch(coreAPI() + "/api/comments", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        })
          .then(function (res) {
            if (!res.ok) {
              return res.json().catch(function () {}).then(function (body) {
                throw new Error((body && body.error) || "HTTP " + res.status);
              });
            }
            if (status) {
              status.hidden = false;
              status.textContent = "评论已提交。";
              status.classList.remove("is-err");
              status.classList.add("is-ok");
            }
            form.reset();
            load();
          })
          .catch(function (err) {
            if (status) {
              status.hidden = false;
              // 服务端 4xx 带具体原因（如 invalid email），直接透出便于自查
              status.textContent = err && err.message
                ? "提交失败：" + err.message
                : "提交失败，请稍后重试。";
              status.classList.add("is-err");
            }
          })
          .then(function () {
            if (btn) btn.disabled = false;
          });
      });
    }

    load();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
