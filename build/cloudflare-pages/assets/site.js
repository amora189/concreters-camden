(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  if (toggle && nav) toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('[data-year]').forEach(node => { node.textContent = new Date().getFullYear(); });
  document.querySelectorAll('form[data-formspree]').forEach(form => {
    const status = form.querySelector('.form-status');
    const submit = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', async event => {
      if (!window.fetch || !status || !submit) return;
      event.preventDefault();
      if (form.dataset.submitting === 'true') return;
      form.dataset.submitting = 'true';
      form.setAttribute('aria-busy', 'true');
      submit.disabled = true;
      status.className = 'form-status';
      status.textContent = 'Sending your enquiry…';
      try {
        const response = await fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) });
        if (!response.ok) throw new Error('Form submission failed');
        form.reset();
        status.className = 'form-status form-status--success';
        status.textContent = 'Thanks — your enquiry has been sent.';
      } catch (error) {
        status.className = 'form-status form-status--error';
        status.textContent = 'We could not send the enquiry. Please check the fields and try again.';
      } finally {
        form.dataset.submitting = 'false';
        form.removeAttribute('aria-busy');
        submit.disabled = false;
      }
    });
  });
})();
