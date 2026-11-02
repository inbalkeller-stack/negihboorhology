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

  // cover title → pink → loader → first neighbourhood (order of the Figma prototype)
  var intro = document.getElementById("intro");
  var title = document.getElementById("cover-title");
  if (intro && title) {
    var PINK_HOLD = 400;      // title stays pink before the dissolve
    var LOADER_TIME = 2700;   // lead burst + fill-up + a short hold
    var timers = [];
    var clear = function () { timers.forEach(clearTimeout); timers = []; };
    var play = function () {
      if (!intro.hidden || timers.length) return;
      title.classList.add("is-hot");
      timers.push(setTimeout(function () {
        intro.hidden = false;            // un-hiding restarts every CSS animation from frame 1
        document.body.style.overflow = "hidden";
        var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        timers.push(setTimeout(function () {
          location.href = intro.getAttribute("data-next");
        }, reduce ? 800 : LOADER_TIME));
      }, PINK_HOLD));
    };
    var stop = function () {
      clear();
      intro.hidden = true;
      title.classList.remove("is-hot");
      document.body.style.overflow = "";
    };
    title.addEventListener("mouseenter", play);
    title.addEventListener("click", play);
    title.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && (timers.length || !intro.hidden)) stop();
    });
    // back button from a neighbourhood: show the plain cover again
    window.addEventListener("pageshow", function (e) { if (e.persisted) stop(); });
  }

  // phone home menu: "x" hides the neighbourhood buttons, tap again to bring them back
  var mMenu = document.getElementById("m-menu"), mToggle = document.getElementById("m-toggle");
  if (mMenu && mToggle) {
    var setMenuH = function () {
      document.documentElement.style.setProperty("--m-menu-h", mMenu.offsetHeight + "px");
    };
    mToggle.addEventListener("click", function () {
      var collapsed = mMenu.classList.toggle("is-collapsed");
      mToggle.textContent = collapsed ? "שכונות" : "x";
      mToggle.setAttribute("aria-expanded", String(!collapsed));
      mToggle.setAttribute("aria-label", collapsed ? "הצגת התפריט" : "הסתרת התפריט");
      setMenuH();
    });
    window.addEventListener("resize", setMenuH);
    setMenuH();
  }
  // bold while pressing — :active alone is unreliable on iOS, so mirror it with a class
  document.querySelectorAll(".press").forEach(function (el) {
    var on = function () { el.classList.add("is-pressed"); };
    var off = function () { el.classList.remove("is-pressed"); };
    el.addEventListener("pointerdown", on);
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { el.addEventListener(t, off); });
  });

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
