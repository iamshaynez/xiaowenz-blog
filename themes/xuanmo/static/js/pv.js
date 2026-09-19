/**
 * 玄墨 · pv.js
 * 页面浏览打点：POST {coreAPI}/api/pv {path, referrer}。
 * 尊重 Do Not Track：navigator.doNotTrack 时不上报。
 */
(function () {
  "use strict";

  if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;
  if (!window.fetch) return;

  var core = (window.XW && window.XW.coreAPI) || "";
  if (!core) return;

  var payload = {
    path: window.location.pathname,
    referrer: document.referrer || ""
  };

  try {
    fetch(core + "/api/pv", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      keepalive: true
    }).catch(function () { /* 打点失败静默 */ });
  } catch (_) { /* ignore */ }
})();
