/* form.js — loading state tombol submit + auto-submit select filter (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  ns.initForm = function () {
    // Loading state: tombol submit disabled + spinner saat form dikirim
    document.querySelectorAll("form").forEach(function (form) {
      form.addEventListener("submit", function () {
        var btn = form.querySelector("[data-submit-button]");
        if (!btn || btn.disabled) return;
        btn.disabled = true;
        var icon = btn.querySelector("i");
        if (icon) {
          icon.className = "fa-solid fa-circle-notch fa-spin text-[13px]";
        }
      });
    });

    // Filter bar: select dengan data-autosubmit langsung mengirim form (GET)
    document.querySelectorAll("select[data-autosubmit]").forEach(function (select) {
      select.addEventListener("change", function () {
        select.closest("form").submit();
      });
    });
  };

  // Skeleton loading: saat form filter (GET) dikirim, daftar diganti baris skeleton
  // agar koneksi DB lambat terasa responsif (DESIGN.md §Loading States)
  ns.initSkeleton = function () {
    document.querySelectorAll("form[data-skeleton]").forEach(function (form) {
      form.addEventListener("submit", function () {
        var container = document.querySelector("[data-skeleton-container]");
        var template = document.querySelector("[data-skeleton-template]");
        if (!container || !template) return;
        var count = container.querySelectorAll("[data-task-item]").length;
        count = Math.min(Math.max(count, 3), 8);
        container.innerHTML = "";
        for (var i = 0; i < count; i++) {
          container.appendChild(template.content.cloneNode(true));
        }
      });
    });
  };
})();
