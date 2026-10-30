(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var navToggle = document.querySelector(".nav-toggle");
  var drawer = document.querySelector(".nav-drawer");
  var overlay = document.querySelector(".nav-overlay");
  var modal = document.getElementById("estimate-modal");
  var sticky = document.querySelector(".sticky-cta");
  var floatBtn = document.querySelector(".float-estimate");
  var lastFocus = null;

  function setMenu(open) {
    if (!drawer || !navToggle) return;
    drawer.classList.toggle("is-open", open);
    if (overlay) overlay.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("menu-open", open);
  }

  function openModal(source) {
    if (!modal) return;
    setMenu(false);
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("modal-open");
    var sourceField = modal.querySelector("[name='_source']");
    if (sourceField && source) sourceField.value = source;
    var first = modal.querySelector("input:not([type='hidden']), select, textarea");
    if (first) first.focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      setMenu(!drawer.classList.contains("is-open"));
    });
  }
  if (overlay) overlay.addEventListener("click", function () { setMenu(false); });

  document.querySelectorAll("[data-open-estimate]").forEach(function (el) {
    el.addEventListener("click", function (event) {
      event.preventDefault();
      openModal(el.getAttribute("data-open-estimate") || "Website");
    });
  });

  document.querySelectorAll("[data-close-modal]").forEach(function (el) {
    el.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      setMenu(false);
      if (modal && !modal.hidden) closeModal();
    }
  });

  document.querySelectorAll(".nav-drawer a").forEach(function (link) {
    link.addEventListener("click", function () { setMenu(false); });
  });

  function bindForm(form) {
    form.addEventListener("submit", function (event) {
      var honey = form.querySelector("[name='_honey']");
      if (honey && honey.value) {
        event.preventDefault();
        return;
      }
      if (!form.hasAttribute("data-mailto")) return;
      event.preventDefault();
      var data = new FormData(form);
      var lines = [];
      ["name", "phone", "email", "service", "city", "message"].forEach(function (key) {
        var value = (data.get(key) || "").toString().trim();
        if (value) lines.push(key + ": " + value);
      });
      var source = (data.get("_source") || "Website").toString();
      lines.push("source: " + source);
      var subject = "Plumbing 101 estimate request";
      var href = "mailto:office@plumbing101.net?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      var note = form.querySelector(".form-note");
      if (note) note.hidden = false;
    });
  }

  document.querySelectorAll("form").forEach(bindForm);

  if (floatBtn) {
    var onScroll = function () {
      var show = window.scrollY > 520;
      floatBtn.classList.toggle("is-visible", show);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".reveal").forEach(function (el) { observer.observe(el); });

  document.querySelectorAll(".faq-item button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item");
      var open = item.classList.contains("is-open");
      document.querySelectorAll(".faq-item").forEach(function (other) {
        other.classList.remove("is-open");
        var b = other.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.querySelectorAll("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var filter = btn.getAttribute("data-filter");
      document.querySelectorAll("[data-filter]").forEach(function (other) {
        other.setAttribute("aria-pressed", other === btn ? "true" : "false");
      });
      document.querySelectorAll("[data-category]").forEach(function (card) {
        var show = filter === "all" || card.getAttribute("data-category") === filter;
        card.hidden = !show;
      });
    });
  });

  document.querySelectorAll(".service-drop > button, .area-drop > button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var parent = btn.parentElement;
      var open = parent.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
})();
