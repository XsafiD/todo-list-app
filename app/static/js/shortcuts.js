/* shortcuts.js — keyboard shortcuts global (spesifikasi di DESIGN.md §Keyboard Shortcuts) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  ns.initShortcuts = function () {
    document.addEventListener("keydown", function (event) {
      if (event.ctrlKey || event.metaKey || event.altKey) return;

      var target = event.target;
      var tag = target.tagName;
      if (
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        target.isContentEditable
      ) {
        return;
      }

      if (event.key === "n") {
        var createUrl = document.body.getAttribute("data-url-task-create");
        if (createUrl) window.location.assign(createUrl);
      } else if (event.key === "/") {
        var filter = document.querySelector("select[data-autosubmit]");
        if (filter) {
          event.preventDefault();
          filter.focus();
        }
      }
    });
  };
})();
