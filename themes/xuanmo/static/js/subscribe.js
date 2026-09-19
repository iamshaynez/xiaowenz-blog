/**
 * 玄墨 · subscribe.js
 * 订阅表单：POST {coreAPI}/api/subscribe（字段 email / name / 蜜罐 website / cf-turnstile-response）。
 * 事件委托，兼容 hugo-extra.js 动态注入的弹层表单；无 JS 时 <form action> 原生提交。
 */
(function () {
  "use strict";

  function coreAPI() {
    return (window.XW && window.XW.coreAPI) || "";
  }

  function statusEl(form) {
    const section = form.closest(".entry-section");
    return section ? section.querySelector(".xw-form-status") : null;
  }

  function setStatus(form, msg, ok) {
    const el = statusEl(form);
    if (!el) return;
    el.hidden = false;
    el.textContent = msg;
    el.classList.toggle("is-ok", !!ok);
    el.classList.toggle("is-err", !ok);
  }

  document.addEventListener("submit", function (e) {
    const form = e.target;
    if (!form || !form.classList || !form.classList.contains("js-subscribe-form")) return;
    if (!window.fetch) return; // 老浏览器回退原生提交
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    const payload = {
      email: (form.elements.email && form.elements.email.value || "").trim(),
      name: (form.elements.name && form.elements.name.value || "").trim(),
      website: (form.elements.website && form.elements.website.value || "").trim() // 蜜罐：正常用户留空
    };
    const ts = form.querySelector('[name="cf-turnstile-response"]');
    if (ts && ts.value) payload["cf-turnstile-response"] = ts.value;

    if (!payload.email) {
      setStatus(form, "请填写邮箱地址。", false);
      return;
    }

    if (btn) btn.disabled = true;
    fetch(coreAPI() + "/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        setStatus(form, "订阅成功，请查收确认邮件。", true);
        form.reset();
      })
      .catch(function () {
        setStatus(form, "提交失败，请稍后重试。", false);
      })
      .then(function () {
        if (btn) btn.disabled = false;
      });
  });
})();
