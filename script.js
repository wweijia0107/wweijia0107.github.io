const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (event) => {
    const target = document.querySelector(anchor.getAttribute("href"));

    if (!target) {
      return;
    }

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth" });

    try {
      history.replaceState(null, "", window.location.pathname + window.location.search);
    } catch {
      // Some local file previews restrict URL cleanup.
    }
  });
});

if (toggle && links) {
  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  links.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

document.getElementById("year").textContent = new Date().getFullYear();
