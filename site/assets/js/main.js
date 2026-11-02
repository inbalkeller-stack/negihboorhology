// שכונולוגיה — popups for the stats panels and the about/credits buttons
(function () {
  "use strict";

  function openDialog(dlg, opener) {
    if (!dlg) return;
    dlg._opener = opener || null;
    if (typeof dlg.showModal === "function") dlg.showModal();
    else dlg.setAttribute("open", "");
  }

  function closeDialog(dlg) {
    if (typeof dlg.close === "function") dlg.close();
    else dlg.removeAttribute("open");
  }

  document.querySelectorAll("dialog").forEach(function (dlg) {
    // close button
    var btn = dlg.querySelector(".dialog-close");
    if (btn) btn.addEventListener("click", function () { closeDialog(dlg); });
    // click outside the content (on the backdrop) closes
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) closeDialog(dlg);
    });
    // return focus to whatever opened it
    dlg.addEventListener("close", function () {
      if (dlg._opener) dlg._opener.focus();
    });
  });

  // cover title: hover (or tap / Enter) turns it pink and plays the loading animation
  var intro = document.getElementById("intro");
  var title = document.getElementById("cover-title");
  if (intro && title) {
    var timer = null;
    var play = function (fromKeyboard) {
      if (!intro.hidden) return;
      title.classList.add("is-hot");
      clearTimeout(timer);
      timer = setTimeout(function () {
        intro.hidden = false;               // un-hiding restarts every CSS animation from frame 1
        document.body.style.overflow = "hidden";
        var start = document.getElementById("intro-start");
        if (start && fromKeyboard === true) start.focus({ preventScroll: true });
      }, 220);
    };
    var stop = function () {
      clearTimeout(timer);
      intro.hidden = true;
      title.classList.remove("is-hot");
      document.body.style.overflow = "";
    };
    title.addEventListener("mouseenter", function () { play(false); });
    title.addEventListener("click", function () { play(false); });
    title.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(true); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !intro.hidden && !document.querySelector("dialog[open]")) stop();
    });
    // coming back with the browser's back button: show the cover, not the frozen animation
    window.addEventListener("pageshow", function (e) { if (e.persisted) stop(); });
  }

  // about / credits on the home page
  document.querySelectorAll("[data-dialog]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      openDialog(document.getElementById(btn.getAttribute("data-dialog")), btn);
    });
  });

  // neighbourhood labels → stats panel
  var panelDlg = document.getElementById("panel-dialog");
  if (panelDlg) {
    var img = panelDlg.querySelector(".panel-img");
    document.querySelectorAll("[data-panel]").forEach(function (btn) {
      // warm the cache so the panel appears instantly
      btn.addEventListener("pointerenter", function () {
        var pre = new Image(); pre.src = btn.getAttribute("data-panel");
      }, { once: true });
      btn.addEventListener("click", function () {
        var name = btn.getAttribute("data-name");
        img.src = btn.getAttribute("data-panel");
        img.alt = "נתוני השכונה " + name;
        panelDlg.setAttribute("aria-label", "נתוני " + name);
        openDialog(panelDlg, btn);
      });
    });
  }

  // phones: scroll the swipeable nav so the current neighbourhood is visible
  var cur = document.querySelector('.stage .nav [aria-current="page"]');
  if (cur && window.matchMedia("(max-width: 900px)").matches) {
    var ul = cur.closest("ul");
    var r = cur.getBoundingClientRect(), u = ul.getBoundingClientRect();
    ul.scrollLeft += (r.left + r.width / 2) - (u.left + u.width / 2);
  }

  // keyboard: ← does what the nav arrow does
  var next = document.querySelector(".nav-next");
  document.addEventListener("keydown", function (e) {
    if (document.querySelector("dialog[open]")) return;
    if (e.target.closest && e.target.closest("input, textarea")) return;
    if (e.key === "ArrowLeft" && next) { location.href = next.href; }
  });
})();
