/* kanban.js — board drag & drop via SortableJS + fallback tombol pindah (12-ajax-js.md) */
(function () {
  "use strict";

  var ns = (window.Dashboardku = window.Dashboardku || {});

  /* Urutan kolom — JAGA SINKRON dengan KANBAN_COLUMNS di task_controller.py */
  var COLUMN_ORDER = ["todo", "in_progress", "done"];

  ns.initKanbanBoard = function () {
    var board = document.querySelector("[data-kanban-board]");
    if (!board || typeof window.Sortable === "undefined") return;

    var csrfInput = board.querySelector("input[name='csrf_token']");

    function columnOf(el) {
      return el.closest("[data-kanban-column]");
    }

    function refreshColumn(column) {
      var cards = column.querySelectorAll("[data-kanban-card]");
      var count = column.querySelector("[data-kanban-count]");
      if (count) count.textContent = String(cards.length);

      var empty = column.querySelector("[data-kanban-empty]");
      if (empty) empty.hidden = cards.length > 0;

      var position = COLUMN_ORDER.indexOf(column.getAttribute("data-kanban-column"));
      cards.forEach(function (card) {
        var prev = card.querySelector("[data-kanban-move='prev']");
        var next = card.querySelector("[data-kanban-move='next']");
        if (prev) prev.classList.toggle("hidden", position <= 0);
        if (next) next.classList.toggle("hidden", position >= COLUMN_ORDER.length - 1);
      });
    }

    function refreshBoard() {
      board.querySelectorAll("[data-kanban-column]").forEach(refreshColumn);
    }

    function save(card, status, revert) {
      card.classList.add("is-loading");
      fetch(card.getAttribute("data-status-url"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "fetch",
          "X-CSRFToken": csrfInput ? csrfInput.value : "",
        },
        body: JSON.stringify({ status: status }),
      })
        .then(function (response) {
          if (!response.ok) throw new Error("Gagal memperbarui status tugas.");
          return response.json();
        })
        .then(function (payload) {
          if (payload.status !== "ok") {
            throw new Error(payload.message || "Gagal memperbarui status tugas.");
          }
          card.classList.toggle("is-done", payload.data.status === "done");
          ns.toast(payload.message, "success");
        })
        .catch(function (err) {
          revert();
          ns.toast(err.message, "error");
        })
        .finally(function () {
          card.classList.remove("is-loading");
          refreshBoard();
        });
    }

    /* Drag antar kolom — reorder dalam kolom sama tidak dipersist (sort: false) */
    board.querySelectorAll("[data-kanban-cards]").forEach(function (list) {
      window.Sortable.create(list, {
        group: "kanban",
        sort: false,
        animation: 150,
        ghostClass: "kanban-ghost",
        dragClass: "kanban-drag",
        onStart: function () {
          board.classList.add("is-dragging");
        },
        onEnd: function (evt) {
          board.classList.remove("is-dragging");
          if (evt.from === evt.to) return;
          var card = evt.item;
          var status = columnOf(evt.to).getAttribute("data-kanban-column");
          var fromList = evt.from;
          var oldIndex = evt.oldIndex;
          save(card, status, function revert() {
            var ref = fromList.children[oldIndex] || null;
            fromList.insertBefore(card, ref);
          });
        },
      });
    });

    /* Fallback keyboard/touch: tombol pindah kolom */
    board.querySelectorAll("[data-kanban-move]").forEach(function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        var card = button.closest("[data-kanban-card]");
        if (!card || card.classList.contains("is-loading")) return;

        var position = COLUMN_ORDER.indexOf(
          columnOf(card).getAttribute("data-kanban-column")
        );
        var target = position + (button.getAttribute("data-kanban-move") === "next" ? 1 : -1);
        if (target < 0 || target >= COLUMN_ORDER.length) return;

        var fromList = card.parentElement;
        var targetList = board.querySelector(
          '[data-kanban-column="' + COLUMN_ORDER[target] + '"] [data-kanban-cards]'
        );
        if (!targetList) return;

        targetList.appendChild(card);
        refreshBoard();
        save(card, COLUMN_ORDER[target], function revert() {
          fromList.appendChild(card);
          refreshBoard();
        });
      });
    });

    refreshBoard();
  };
})();
