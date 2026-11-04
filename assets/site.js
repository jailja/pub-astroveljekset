(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById('theme-toggle');
  const savedTheme = (() => { try { return localStorage.getItem('astroveljekset-theme'); } catch { return null; } })();
  if (savedTheme === 'light' || savedTheme === 'dark') root.dataset.theme = savedTheme;

  function updateThemeButton() {
    if (!themeButton) return;
    const light = root.dataset.theme === 'light';
    themeButton.setAttribute('aria-label', light ? 'Vaihda tummaan teemaan' : 'Vaihda vaaleaan teemaan');
    themeButton.title = light ? 'Vaihda tummaan teemaan' : 'Vaihda vaaleaan teemaan';
    themeButton.querySelector('span').textContent = light ? '☾' : '☼';
  }
  updateThemeButton();
  themeButton?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('astroveljekset-theme', root.dataset.theme); } catch { /* storage unavailable */ }
    updateThemeButton();
  });

  const layout = document.getElementById('reader-layout');
  const tocToggle = document.getElementById('toc-toggle');
  const backdrop = document.getElementById('sidebar-backdrop');
  const setNavOpen = (open) => {
    if (!layout || !tocToggle) return;
    layout.classList.toggle('nav-open', open);
    tocToggle.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  };
  tocToggle?.addEventListener('click', () => setNavOpen(!layout.classList.contains('nav-open')));
  backdrop?.addEventListener('click', () => setNavOpen(false));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setNavOpen(false); });

  const progress = document.getElementById('reading-progress');
  const article = document.querySelector('.chapter-article');
  const chapter = document.querySelector('[data-chapter]')?.getAttribute('data-chapter');
  if (progress && article) {
    let scheduled = false;
    const update = () => {
      const start = article.offsetTop;
      const end = start + article.offsetHeight - window.innerHeight;
      const value = end <= start ? 1 : Math.min(1, Math.max(0, (window.scrollY - start) / (end - start)));
      progress.style.transform = `scaleX(${value})`;
      scheduled = false;
      if (chapter !== null && chapter !== undefined) {
        try { localStorage.setItem('astroveljekset-last-chapter', chapter); } catch { /* storage unavailable */ }
      }
    };
    const requestUpdate = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
    requestUpdate();
  }

  const startButton = document.querySelector('.button-primary');
  if (startButton && !chapter) {
    try {
      const last = Number(localStorage.getItem('astroveljekset-last-chapter'));
      if (Number.isInteger(last) && last > 0 && last <= 25) {
        const link = document.querySelector(`.toc-grid li:nth-child(${last}) a`);
        if (link) {
          startButton.href = link.getAttribute('href');
          startButton.firstChild.textContent = 'Jatka lukemista ';
        }
      }
    } catch { /* storage unavailable */ }
  }
})();
