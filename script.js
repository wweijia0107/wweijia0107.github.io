(function () {
  document.documentElement.classList.add('js');
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.section-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.querySelector('span').textContent = isOpen ? '−' : '+';
  });
  for (const a of nav.querySelectorAll('a')) {
    a.addEventListener('click', () => { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
  }
  if ('IntersectionObserver' in window) {
    const links = new Map([...nav.querySelectorAll('a[href^="#"]')].map(a => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver(entries => {
      for (const entry of entries) {
        const link = links.get(entry.target.id);
        if (!link) continue;
        if (entry.isIntersecting) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      }
    }, {rootMargin: '-8% 0px -70% 0px'});
    document.querySelectorAll('main section[id]').forEach(section => io.observe(section));
  }
})();
