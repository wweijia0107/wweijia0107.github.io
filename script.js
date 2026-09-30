document.documentElement.classList.add("js");

const toggle = document.querySelector(".nav-toggle");
const navigation = document.querySelector(".section-nav");

function closeNavigation() {
  navigation.classList.remove("open");
  toggle.setAttribute("aria-expanded", "false");
  toggle.querySelector("span").textContent = "+";
}

if (toggle && navigation) {
  toggle.addEventListener("click", () => {
    const open = navigation.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector("span").textContent = open ? "−" : "+";
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeNavigation();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navigation.classList.contains("open")) {
      closeNavigation();
      toggle.focus();
    }
  });
}

// Native anchor links retain shareable section URLs and keyboard behavior.
if (navigation && "IntersectionObserver" in window) {
  const sectionLinks = [...navigation.querySelectorAll("a")];
  const sections = [...document.querySelectorAll("main > section[id]")];
  const visibleSections = new Set();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) visibleSections.add(entry.target.id);
      else visibleSections.delete(entry.target.id);
    });
    const current = [...sections].reverse().find((section) => visibleSections.has(section.id));
    if (!current) return;
    sectionLinks.forEach((link) => {
      if (link.hash === `#${current.id}`) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }, { rootMargin: "-8% 0px -65% 0px" });
  sections.forEach((section) => observer.observe(section));
}

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();
