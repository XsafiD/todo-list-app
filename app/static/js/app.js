/* app.js — entry point: DOM ready gate + init semua modul (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  function init() {
    Object.keys(ns).forEach(function (key) {
      if (key.indexOf("init") === 0 && typeof ns[key] === "function") {
        try {
          ns[key]();
        } catch (err) {
          console.error("[Dashboardku] Gagal init " + key + ":", err);
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
