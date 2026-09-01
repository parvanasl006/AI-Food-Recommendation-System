document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const themeToggle = document.querySelector('.theme-toggle');

  if (themeToggle) {
    const savedTheme = localStorage.getItem('moodmeal-theme');

    if (savedTheme === 'light') {
      body.classList.add('light-mode');
      themeToggle.textContent = '☀️';
    } else {
      themeToggle.textContent = '🌙';
    }

    themeToggle.addEventListener('click', () => {
      const isLight = body.classList.toggle('light-mode');
      localStorage.setItem('moodmeal-theme', isLight ? 'light' : 'dark');
      themeToggle.textContent = isLight ? '☀️' : '🌙';
    });
  }

  const revealElements = document.querySelectorAll('.reveal-on-scroll');

  if (revealElements.length) {
    if ('IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });

      revealElements.forEach((element) => revealObserver.observe(element));
    } else {
      revealElements.forEach((element) => element.classList.add('visible'));
    }
  }

  document.querySelectorAll('[data-scroll-target]').forEach((button) => {
    button.addEventListener('click', (event) => {
      const targetSelector = button.getAttribute('data-scroll-target');
      if (!targetSelector || targetSelector === '#') return;

      const target = document.querySelector(targetSelector);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});