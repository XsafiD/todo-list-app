/* modal.js — open/close modal + overlay click + Escape + body scroll lock + fokus trap (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  function focusablesIn(modal) {
    return Array.prototype.filter.call(
      modal.querySelectorAll("button, [href], input, select, textarea"),
      function (el) {
        return !el.disabled && el.offsetParent !== null;
      }
    );
  }

  function openModal(modal) {
    modal._opener = document.activeElement;
    modal.classList.remove("hidden");
    modal.classList.add("flex", "is-open");
    document.body.style.overflow = "hidden";
    var focusables = focusablesIn(modal);
    if (focusables.length) focusables[0].focus();
  }

  function closeModal(modal) {
    modal.classList.remove("is-open");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    if (!document.querySelector("[data-modal].is-open")) {
      document.body.style.overflow = "";
    }
    if (modal._opener && modal._opener.parentNode) {
      modal._opener.focus();
      modal._opener = null;
    }
  }

  ns.initModal = function () {
    document.querySelectorAll("[data-modal-target]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var modal = document.getElementById(btn.getAttribute("data-modal-target"));
        if (modal) openModal(modal);
      });
    });

    document.querySelectorAll("[data-modal]").forEach(function (modal) {
      var overlay = modal.querySelector("[data-modal-overlay]");
      if (overlay) {
        overlay.addEventListener("click", function () {
          closeModal(modal);
        });
      }
      modal.querySelectorAll("[data-modal-close]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          closeModal(modal);
        });
      });
    });

    document.addEventListener("keydown", function (event) {
      var modal = document.querySelector("[data-modal].is-open");
      if (!modal) return;

      if (event.key === "Escape") {
        closeModal(modal);
        return;
      }
      if (event.key !== "Tab") return;

      // Fokus trap: siklus Tab tetap di dalam modal
      var focusables = focusablesIn(modal);
      if (!focusables.length) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  };
})();
