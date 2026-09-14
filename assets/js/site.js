/* Pilotech — interactions (vanilla, sans dépendance). */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Menus déroulants (desktop) : survol géré en CSS, clavier ici. */
  function initMenus() {
    document.querySelectorAll("[data-menu]").forEach(function (menu) {
      var trigger = menu.querySelector("a[aria-haspopup]");
      if (!trigger) return;
      function set(open) {
        menu.classList.toggle("is-open", open);
        trigger.setAttribute("aria-expanded", open ? "true" : "false");
      }
      menu.addEventListener("mouseenter", function () { set(true); });
      menu.addEventListener("mouseleave", function () { set(false); });
      menu.addEventListener("focusin", function () { set(true); });
      menu.addEventListener("focusout", function (e) { if (!menu.contains(e.relatedTarget)) set(false); });
      trigger.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); set(true); var first = menu.querySelector(".menu-panel a"); if (first) first.focus(); }
      });
      menu.addEventListener("keydown", function (e) { if (e.key === "Escape") { set(false); trigger.focus(); } });
    });
  }

  /* Tiroir mobile */
  function initDrawer() {
    var drawer = document.getElementById("drawer");
    var openBtn = document.querySelector("[data-drawer-open]");
    var closeBtn = document.querySelector("[data-drawer-close]");
    var backdrop = document.querySelector("[data-drawer-backdrop]");
    if (!drawer || !openBtn) return;
    function show() {
      drawer.classList.add("is-open"); drawer.setAttribute("aria-hidden", "false");
      openBtn.setAttribute("aria-expanded", "true");
      if (backdrop) backdrop.classList.remove("hidden");
      document.body.classList.add("overflow-hidden");
      if (closeBtn) closeBtn.focus();
    }
    function hide() {
      drawer.classList.remove("is-open"); drawer.setAttribute("aria-hidden", "true");
      openBtn.setAttribute("aria-expanded", "false");
      if (backdrop) backdrop.classList.add("hidden");
      document.body.classList.remove("overflow-hidden");
      openBtn.focus();
    }
    openBtn.addEventListener("click", show);
    if (closeBtn) closeBtn.addEventListener("click", hide);
    if (backdrop) backdrop.addEventListener("click", hide);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) hide(); });
  }

  /* Galerie produit : vignettes, flèches, clavier, balayage */
  function initGallery() {
    document.querySelectorAll("[data-gallery]").forEach(function (root) {
      var main = root.querySelector("[data-gallery-main]");
      var thumbs = Array.prototype.slice.call(root.querySelectorAll("[data-gallery-thumb]"));
      var counter = root.querySelector("[data-gallery-counter]");
      if (!main || thumbs.length < 2) return;
      var index = 0;
      function show(i) {
        index = (i + thumbs.length) % thumbs.length;
        var t = thumbs[index];
        main.style.opacity = "0";
        var swap = function () { main.src = t.getAttribute("data-src"); main.alt = t.getAttribute("data-alt") || ""; main.style.opacity = "1"; };
        reduce ? swap() : window.setTimeout(swap, 120);
        thumbs.forEach(function (b, k) { b.classList.toggle("is-current", k === index); b.setAttribute("aria-current", k === index ? "true" : "false"); });
        if (counter) counter.textContent = (index + 1) + " / " + thumbs.length;
        t.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduce ? "auto" : "smooth" });
      }
      thumbs.forEach(function (b, i) { b.addEventListener("click", function () { show(i); }); });
      var prev = root.querySelector("[data-gallery-prev]"), next = root.querySelector("[data-gallery-next]");
      if (prev) prev.addEventListener("click", function () { show(index - 1); });
      if (next) next.addEventListener("click", function () { show(index + 1); });
      root.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { e.preventDefault(); show(index - 1); }
        if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
      });
      var x0 = null;
      main.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      main.addEventListener("touchend", function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 45) show(dx < 0 ? index + 1 : index - 1);
        x0 = null;
      }, { passive: true });
    });
  }

  /* Onglets « par type de logement » */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (root) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll("[data-tab]"));
      var panels = Array.prototype.slice.call(root.querySelectorAll("[data-tab-content]"));
      function activate(name, focus) {
        tabs.forEach(function (t) {
          var on = t.getAttribute("data-tab") === name;
          t.setAttribute("aria-selected", on ? "true" : "false");
          t.setAttribute("tabindex", on ? "0" : "-1");
          if (on && focus) t.focus();
        });
        panels.forEach(function (p) { p.hidden = p.getAttribute("data-tab-content") !== name; });
      }
      tabs.forEach(function (t, i) {
        t.addEventListener("click", function () { activate(t.getAttribute("data-tab"), false); });
        t.addEventListener("keydown", function (e) {
          var j = i;
          if (e.key === "ArrowRight") j = (i + 1) % tabs.length;
          else if (e.key === "ArrowLeft") j = (i - 1 + tabs.length) % tabs.length;
          else if (e.key === "Home") j = 0;
          else if (e.key === "End") j = tabs.length - 1;
          else return;
          e.preventDefault(); activate(tabs[j].getAttribute("data-tab"), true);
        });
      });
      if (tabs.length) activate(tabs[0].getAttribute("data-tab"), false);
    });
  }

  /* Frise des étapes : le trait suit le défilement */
  function initSteps() {
    var lists = document.querySelectorAll("[data-steps]");
    if (!lists.length) return;
    lists.forEach(function (list) {
      var steps = Array.prototype.slice.call(list.querySelectorAll("[data-step]"));
      if (!steps.length) return;
      if (reduce) { steps.forEach(function (s) { s.classList.add("is-active"); }); list.style.setProperty("--steps-progress", "100%"); return; }
      function update() {
        var trigger = window.innerHeight * 0.66, reached = 0;
        steps.forEach(function (s, i) { var on = s.getBoundingClientRect().top < trigger; s.classList.toggle("is-active", on); if (on) reached = i + 1; });
        var pct = 0;
        if (reached) {
          var box = list.getBoundingClientRect(), last = steps[reached - 1].getBoundingClientRect();
          pct = Math.max(0, Math.min(100, ((last.top + 20) - box.top) / box.height * 100));
        }
        list.style.setProperty("--steps-progress", pct + "%");
      }
      var ticking = false;
      function onScroll() { if (ticking) return; ticking = true; window.requestAnimationFrame(function () { update(); ticking = false; }); }
      window.addEventListener("scroll", onScroll, { passive: true });
      window.addEventListener("resize", onScroll);
      update();
    });
  }

  /* Formulaires : validation native avec messages en français */
  function initForms() {
    document.querySelectorAll("form[novalidate]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        if (form.checkValidity()) return;
        e.preventDefault();
        var first = form.querySelector(":invalid");
        if (first) { first.focus(); first.reportValidity(); }
      });
    });
  }

  /* Mode sombre : bouton, mémorisation, synchronisation avec le réglage système */
  function initTheme() {
    var root = document.documentElement;
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    function apply(dark, persist) {
      root.classList.toggle("dark", dark);
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", dark ? "true" : "false"); });
      if (persist) { try { localStorage.setItem("theme", dark ? "dark" : "light"); } catch (e) {} }
    }
    buttons.forEach(function (b) { b.addEventListener("click", function () { apply(!root.classList.contains("dark"), true); }); });
    apply(root.classList.contains("dark"), false);
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function (e) { try { if (!localStorage.getItem("theme")) apply(e.matches, false); } catch (err) {} };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
  }

  /* Préchargeur : affiché au premier chargement de la session, retiré une fois la page chargée */
  function initPreloader() {
    var el = document.getElementById("preloader");
    if (!el) return;
    if (document.documentElement.classList.contains("no-preloader")) { el.remove(); return; }
    var start = Date.now(), minShown = reduce ? 0 : 900, finished = false;
    function done() {
      if (finished) return; finished = true;
      el.classList.add("is-done");
      try { sessionStorage.setItem("pilotech-loaded", "1"); } catch (e) {}
      window.setTimeout(function () { el.remove(); }, 700);
    }
    function finish() { window.setTimeout(done, Math.max(0, minShown - (Date.now() - start))); }
    if (document.readyState === "complete") finish(); else window.addEventListener("load", finish);
    window.setTimeout(done, 3500); /* filet de sécurité si une ressource externe traîne */
  }

  function init() { initTheme(); initPreloader(); initMenus(); initDrawer(); initGallery(); initTabs(); initSteps(); initForms(); }
  if (document.readyState !== "loading") init(); else document.addEventListener("DOMContentLoaded", init);
})();
