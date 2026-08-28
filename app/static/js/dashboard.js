/* dashboard.js — alert/flash behavior: auto-dismiss + tombol tutup (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  ns.initAlert = function () {
    document.querySelectorAll("[data-alert]").forEach(function (alert) {
      var close = alert.querySelector("[data-alert-close]");
      if (close) {
        close.addEventListener("click", function () {
          alert.remove();
        });
      }
      // Auto-dismiss setelah 4 detik
      window.setTimeout(function () {
        alert.style.transition = "opacity 150ms ease-out";
        alert.style.opacity = "0";
        window.setTimeout(function () {
          alert.remove();
        }, 200);
      }, 4000);
    });
  };
})();
