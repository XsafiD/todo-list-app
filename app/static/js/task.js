/* task.js — toggle complete via AJAX: update in-place + toast, tanpa reload (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  /* Peta badge status — JAGA SINKRON dengan macro status_badge di components/badge.html */
  var STATUS_BADGES = {
    todo: {
      cls: "border border-hairline bg-surface-soft text-slate",
      icon: "fa-regular fa-circle",
      label: "Todo",
    },
    in_progress: {
      cls: "bg-info/10 text-info-ink",
      icon: "fa-solid fa-spinner",
      label: "Sedang Dikerjakan",
    },
    done: {
      cls: "bg-success/10 text-success-ink",
      icon: "fa-solid fa-circle-check",
      label: "Selesai",
    },
  };

  function badgeHtml(status) {
    var m = STATUS_BADGES[status] || STATUS_BADGES.todo;
    return (
      '<span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[12px] font-medium ' +
      m.cls +
      '"><i class="' +
      m.icon +
      ' text-[11px]" aria-hidden="true"></i>' +
      m.label +
      "</span>"
    );
  }

  function applyStatus(row, status) {
    row.setAttribute("data-status", status);
    row.classList.toggle("is-done", status === "done");

    var icon = row.querySelector("[data-task-toggle-icon]");
    if (icon) {
      icon.className =
        (status === "done" ? "fa-solid" : "fa-regular") + " fa-circle-check";
    }

    var button = row.querySelector("[data-task-toggle]");
    if (button) {
      button.setAttribute(
        "aria-label",
        status === "done" ? "Buka kembali tugas" : "Tandai selesai"
      );
    }

    var badge = row.querySelector("[data-task-status-badge]");
    if (badge) {
      badge.innerHTML = badgeHtml(status);
    }
  }

  ns.initTaskToggle = function () {
    document.querySelectorAll("[data-task-toggle]").forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        var form = button.closest("form");
        var row = button.closest("[data-task-item]");
        if (!form || !row || row.classList.contains("is-loading")) return;

        var csrf = form.querySelector("input[name='csrf_token']");
        row.classList.add("is-loading");
        fetch(form.getAttribute("action"), {
          method: "POST",
          headers: {
            "X-Requested-With": "fetch",
            "X-CSRFToken": csrf ? csrf.value : "",
          },
        })
          .then(function (response) {
            if (!response.ok) throw new Error("Gagal memperbarui tugas");
            return response.json();
          })
          .then(function (payload) {
            if (payload.status !== "ok") {
              throw new Error(payload.message || "Gagal memperbarui tugas");
            }
            applyStatus(row, payload.data.status);
            ns.toast(payload.message, "success");
          })
          .catch(function (err) {
            ns.toast(err.message, "error");
          })
          .finally(function () {
            row.classList.remove("is-loading");
          });
      });
    });
  };
})();
