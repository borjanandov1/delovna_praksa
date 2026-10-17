(function () {
  "use strict";

  var CONSENT_KEY = "forge_cookie_consent";

  function readConsent() {
    try {
      return window.localStorage.getItem(CONSENT_KEY);
    } catch (e) {
      var m = document.cookie.match(/(?:^|;\s*)forge_cookie_consent=([^;]*)/);
      return m ? decodeURIComponent(m[1]) : null;
    }
  }

  function writeConsent(value) {
    try {
      window.localStorage.setItem(CONSENT_KEY, value);
    } catch (e) {}

    var secure = window.location.protocol === "https:" ? "; Secure" : "";
    document.cookie =
      CONSENT_KEY + "=" + encodeURIComponent(value) +
      "; path=/; max-age=" + (60 * 60 * 24 * 365) + "; SameSite=Lax" + secure;
  }

  function initCookies() {
    var banner = document.getElementById("cookieBanner");
    if (!banner) return;

    function show() {
      banner.hidden = false;

      requestAnimationFrame(function () {
        requestAnimationFrame(function () { banner.classList.add("is-visible"); });
      });
    }

    function hide() {
      banner.classList.remove("is-visible");
      window.setTimeout(function () { banner.hidden = true; }, 400);
    }

    if (!readConsent()) show();

    banner.querySelectorAll("[data-cookie-accept]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var choice = btn.getAttribute("data-cookie-accept");
        writeConsent(choice);
        hide();
        if (choice === "all") enableAnalytics();
      });
    });

    document.querySelectorAll("[data-cookie-reopen]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        show();
      });
    });

    if (readConsent() === "all") enableAnalytics();
  }

  function enableAnalytics() {
    if (window.__forgeAnalyticsLoaded) return;
    window.__forgeAnalyticsLoaded = true;
  }

  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });

    items.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 70 + "ms";
      io.observe(el);
    });
  }

  function initNav() {
    var collapse = document.getElementById("mainNav");
    if (!collapse) return;
    collapse.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (!collapse.classList.contains("show")) return;
        var inst = bootstrap.Collapse.getInstance(collapse);
        if (inst) inst.hide();
      });
    });
  }

  function boot() {
    initCookies();
    initReveal();
    initNav();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  document.body.addEventListener("htmx:afterSwap", initReveal);
})();
