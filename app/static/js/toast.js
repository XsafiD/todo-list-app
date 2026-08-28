/* toast.js — notifikasi singkat untuk aksi cepat tanpa reload (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  var ICONS = {
    success: "fa-solid fa-circle-check",
    error: "fa-solid fa-circle-exclamation",
    info: "fa-solid fa-circle-info",
  };

  var CLS = {
    success: "border-success/20 bg-success/10 text-success-ink",
    error: "border-critical/20 bg-critical/10 text-critical-ink",
    info: "border-info/20 bg-info/10 text-info-ink",
  };

  function buildContainer() {
    var container = document.querySelector("[data-toast-container]");
    if (container) return container;
    container = document.createElement("div");
    container.setAttribute("data-toast-container", "");
    container.setAttribute("role", "status");
    container.setAttribute("aria-live", "polite");
    container.className =
      "fixed bottom-20 right-4 z-50 flex w-full max-w-xs flex-col gap-2 md:bottom-6";
    document.body.appendChild(container);
    return container;
  }

  function dismiss(toast) {
    toast.style.transition = "opacity 150ms ease-out";
    toast.style.opacity = "0";
    window.setTimeout(function () {
      toast.remove();
    }, 200);
  }

  ns.toast = function (message, type) {
    type = CLS[type] ? type : "info";
    var container = buildContainer();
    var toast = document.createElement("div");
    toast.setAttribute("data-toast", "");
    toast.className =
      "toast pointer-events-auto flex items-center gap-3 rounded-lg border px-4 py-3 text-[14px] " +
      CLS[type];
    var icon = document.createElement("i");
    icon.className = ICONS[type];
    icon.setAttribute("aria-hidden", "true");
    var text = document.createElement("p");
    text.className = "flex-1";
    text.textContent = message;
    var close = document.createElement("button");
    close.type = "button";
    close.setAttribute("data-toast-close", "");
    close.setAttribute("aria-label", "Tutup");
    close.className = "opacity-50 transition hover:opacity-100";
    var closeIcon = document.createElement("i");
    closeIcon.className = "fa-solid fa-xmark";
    closeIcon.setAttribute("aria-hidden", "true");
    close.appendChild(closeIcon);
    toast.appendChild(icon);
    toast.appendChild(text);
    toast.appendChild(close);
    close.addEventListener("click", function () {
      dismiss(toast);
    });
    container.appendChild(toast);
    window.setTimeout(function () {
      if (toast.parentNode) dismiss(toast);
    }, 4000);
  };

  ns.initToast = function () {
    buildContainer();
  };
})();
