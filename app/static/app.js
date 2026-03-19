function qs(name) {
  const u = new URL(window.location.href);
  return u.searchParams.get(name);
}

function showToast(text) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = text;
  el.classList.add("show");
  window.setTimeout(() => el.classList.remove("show"), 2500);
}

function bindRevealButtons() {
  document.querySelectorAll("[data-reveal]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const id = btn.getAttribute("data-reveal");
      const input = document.getElementById(id);
      if (!input) return;
      const isPw = input.getAttribute("type") === "password";
      input.setAttribute("type", isPw ? "text" : "password");
      btn.textContent = isPw ? "Hide" : "Show";
    });
  });
}

function bindDaysPickers() {
  const dayOrder = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  document.querySelectorAll("[data-days-picker]").forEach((picker) => {
    const hidden = picker.previousElementSibling;
    if (!hidden || !hidden.hasAttribute("data-days-input")) return;

    const selected = new Set(
      String(hidden.value || "")
        .split(",")
        .map((d) => d.trim())
        .filter((d) => dayOrder.includes(d))
    );

    const sync = () => {
      picker.querySelectorAll("[data-day]").forEach((btn) => {
        const day = btn.getAttribute("data-day");
        btn.classList.toggle("active", selected.has(day));
      });
      hidden.value = dayOrder.filter((d) => selected.has(d)).join(",");
    };

    picker.querySelectorAll("[data-day]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const day = btn.getAttribute("data-day");
        if (!day) return;
        if (selected.has(day)) {
          selected.delete(day);
        } else {
          selected.add(day);
        }
        sync();
      });
    });

    sync();
  });
}

window.addEventListener("DOMContentLoaded", () => {
  bindRevealButtons();
  bindDaysPickers();
  if (qs("saved") === "1") showToast("Settings saved");
  if (qs("ran") === "1") showToast("Run triggered");
  if (qs("test") === "sonarr_ok") showToast("Sonarr OK");
  if (qs("test") === "sonarr_fail") showToast("Sonarr failed");
  if (qs("test") === "radarr_ok") showToast("Radarr OK");
  if (qs("test") === "radarr_fail") showToast("Radarr failed");
  if (qs("test") === "emby_ok") showToast("Emby OK");
  if (qs("test") === "emby_fail") showToast("Emby failed");
});

