/**
 * 玄墨 · hugo-extra.js
 * Hugo 专属增量交互（不动 main.js）：
 * Enjoy 按钮 · 分享链接 · 订阅弹层（首页「订阅本刊」）
 */
(function () {
  "use strict";

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }
  function qsa(sel, root) {
    return Array.from((root || document).querySelectorAll(sel));
  }

  /* ---------- Enjoy：本地记忆的一次性点赞（无后端，装饰性） ---------- */
  function bindEnjoy() {
    const btn = qs(".js-enjoy");
    if (!btn) return;
    const key = "xw:enjoy:" + window.location.pathname;
    try {
      if (window.localStorage.getItem(key)) btn.disabled = true;
    } catch (_) {}
    btn.addEventListener("click", () => {
      btn.disabled = true;
      try {
        window.localStorage.setItem(key, "1");
      } catch (_) {}
    });
  }

  /* ---------- 分享链接 ---------- */
  function bindShare() {
    qsa(".js-share").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        const url = window.location.href;
        const title = document.title;
        const type = a.dataset.type;
        let target = "";
        if (type === "tw") {
          target = "https://twitter.com/intent/tweet?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(title);
        } else if (type === "wb") {
          target = "https://service.weibo.com/share/share.php?url=" + encodeURIComponent(url) + "&title=" + encodeURIComponent(title);
        } else if (type === "tg") {
          target = "https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(title);
        } else if (type === "wx") {
          // 微信无 Web 分享端点：复制链接
          const done = () => {
            a.setAttribute("aria-label", "链接已复制");
            setTimeout(() => a.setAttribute("aria-label", "分享到微信"), 1600);
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(done, done);
          }
          return;
        }
        if (target) window.open(target, "_blank", "noopener,noreferrer,width=640,height=480");
      });
    });
  }

  /* ---------- 订阅弹层：首页「订阅本刊」按钮 ---------- */
  function buildModal() {
    const tpl = qs(".entry-section.subscribe form");
    const core = (window.XW && window.XW.coreAPI) || "";
    const tsKey = (window.XW && window.XW.turnstileSiteKey) || "";
    const modal = document.createElement("div");
    modal.className = "xw-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "订阅本刊");
    modal.innerHTML =
      '<div class="xw-modal__backdrop" aria-hidden="true"></div>' +
      '<div class="xw-modal__panel">' +
      '<button class="xw-modal__close" type="button" aria-label="关闭">' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>' +
      "</button>" +
      '<section class="entry-section subscribe"><div class="inner"><h2>Subscribe</h2>' +
      '<form method="post" action="' + core + '/api/subscribe" class="js-subscribe-form">' +
      '<input name="name" placeholder="Your name" autocomplete="name">' +
      '<input name="email" type="email" placeholder="Your email address" required autocomplete="email">' +
      '<input name="website" type="text" class="xw-hp" value="" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      (tsKey ? '<div class="cf-turnstile" data-sitekey="' + tsKey + '"></div>' : "") +
      "<button type=\"submit\">Subscribe</button>" +
      "</form>" +
      '<p class="xw-form-status" role="status" aria-live="polite" hidden></p>' +
      "</div></section>" +
      "</div>";
    document.body.appendChild(modal);

    function close() {
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    }
    qs(".xw-modal__backdrop", modal).addEventListener("click", close);
    qs(".xw-modal__close", modal).addEventListener("click", close);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("is-open")) close();
    });
    // 新注入的表单交给 subscribe.js（它用事件委托监听 submit）
    return modal;
  }

  function bindSubscribeModal() {
    const buttons = qsa("button.js-subscribe");
    if (!buttons.length) return;
    // 页面上已有内联订阅表单时（文章页），按钮直接滚动过去；否则开弹层
    const inline = qs(".entry-section.subscribe");
    let modal = null;
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        if (inline) {
          inline.scrollIntoView({ behavior: "smooth", block: "center" });
          const email = qs('input[name="email"]', inline);
          if (email) setTimeout(() => email.focus({ preventScroll: true }), 450);
          return;
        }
        if (!modal) modal = buildModal();
        modal.classList.add("is-open");
        document.body.style.overflow = "hidden";
        // 弹层里的 Turnstile 容器需可见后显式渲染（隐式渲染只管页面加载时已在 DOM 里的）
        const tsBox = qs(".cf-turnstile", modal);
        if (tsBox && window.turnstile && !tsBox.hasAttribute("data-xw-ts-rendered")) {
          tsBox.setAttribute("data-xw-ts-rendered", "1");
          window.turnstile.render(tsBox);
        }
        const email = qs('input[name="email"]', modal);
        if (email) setTimeout(() => email.focus(), 60);
      });
    });
  }

  function init() {
    bindEnjoy();
    bindShare();
    bindSubscribeModal();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
