// custom.js
document.addEventListener('DOMContentLoaded', () => {
  // Плавное появление элементов fade-in
  document.querySelectorAll('.fade-in').forEach(el => {
    el.classList.add('visible');
  });

  // Подтверждение перед удалением
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (!confirm('Вы уверены, что хотите удалить это объявление?')) {
        e.preventDefault();
      }
    });
  });

  // Изменение текста кнопки при отправке формы
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Отправка...';
      }
    });
  });

  // Плавющая кнопка "Наверх"
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  window.onscroll = function() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
      scrollTopBtn.style.display = "block";
    } else {
      scrollTopBtn.style.display = "none";
    }
  };
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Инициализация Bootstrap подсказок (tooltip)
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});