/* Comportamiento común a todas las páginas del sitio */
(function () {
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const SPRITE = (document.body.dataset.raiz || '') + 'images/marca/iconos.svg';

  // ---- Iconos: <i class="fa-solid fa-nombre"> -> SVG del sprite propio ----
  function iconos(ctx = document) {
    $$('i[class*="fa-"]', ctx).forEach(i => {
      const nombre = (i.className.match(/fa-(?!solid|regular|brands)([a-z0-9-]+)/) || [])[1];
      if (!nombre) return;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ico-svg ' + i.className.replace(/fa-[a-z0-9-]+/g, '').trim());
      svg.setAttribute('aria-hidden', 'true'); svg.setAttribute('focusable', 'false');
      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttribute('href', SPRITE + '#' + nombre);
      svg.appendChild(use);
      if (i.getAttribute('style')) svg.setAttribute('style', i.getAttribute('style'));
      i.replaceWith(svg);
    });
  }
  window.iconos = iconos;

  // ---- Espacios para imágenes (data-imagen / data-alt / data-pie / data-pie2 / data-sugerencia) ----
  function espaciosImagen() {
    $$('.tile-imagen').forEach(fig => {
      const src = fig.dataset.imagen;
      if (src) {
        const img = new Image();
        const base = src.replace(/\.(jpe?g|png)$/i, '');
        img.src = base + '-full.webp'; img.alt = fig.dataset.alt || ''; img.loading = 'lazy'; img.decoding = 'async';
        img.onerror = () => { img.onerror = null; img.src = src; };
        fig.prepend(img);
        if (fig.dataset.pie) {
          const cap = document.createElement('figcaption');
          cap.className = 'pie';
          cap.innerHTML = `<strong>${fig.dataset.pie}</strong>${fig.dataset.pie2 ? `<span>${fig.dataset.pie2}</span>` : ''}`;
          fig.appendChild(cap);
        }
      } else {
        fig.classList.add('pendiente');
        fig.innerHTML = `<div class="imagen-pendiente"><i class="fa-regular fa-image" aria-hidden="true"></i><strong>Espacio para poner imagen</strong></div>`;
      }
    });
  }

  // ---- Aparición escalonada ----
  function aparicion() {
    $$('.bento').forEach(grid => $$('.reveal', grid).forEach((el, i) => el.style.setProperty('--retraso', `${Math.min(i, 8) * 70}ms`)));
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    $$('.reveal').forEach(el => io.observe(el));
    // Respaldo: si el observador no corre (pestaña oculta, navegador viejo), muestra lo que ya está en pantalla
    const respaldo = () => $$('.reveal:not(.in)').forEach(el => { const r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) { el.classList.add('in'); io.unobserve(el); } });
    setTimeout(respaldo, 1200);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') setTimeout(respaldo, 300); });
  }

  // ---- Contador ----
  function contadores() {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target, meta = +el.dataset.meta || 0; io.unobserve(el);
        if (reduceMotion) { el.textContent = meta; return; }
        const inicio = performance.now(), dur = 1100;
        const paso = t => { const p = Math.min(1, (t - inicio) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(meta * e); if (p < 1) requestAnimationFrame(paso); };
        requestAnimationFrame(paso);
      });
    }, { threshold: 0.6 });
    $$('.contador').forEach(el => io.observe(el));
  }

  // ---- Topbar y menú móvil ----
  function menu() {
    const topbar = $('.topbar'), toggle = $('.menu-toggle'), drawer = $('#mobile-drawer'), overlay = $('.drawer-overlay'), closeBtn = $('.drawer-close');
    const onScroll = () => topbar?.classList.toggle('is-scrolled', window.scrollY > 6);
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
    if (!toggle || !drawer) return;
    let scrollY = 0;
    const abrir = () => { scrollY = window.scrollY || 0; drawer.classList.add('open'); overlay.hidden = false; toggle.classList.add('active'); drawer.setAttribute('aria-hidden', 'false'); toggle.setAttribute('aria-expanded', 'true'); document.body.classList.add('menu-open-fixed'); drawer.querySelector('.drawer-link')?.focus(); };
    const cerrar = () => { drawer.classList.remove('open'); overlay.hidden = true; toggle.classList.remove('active'); drawer.setAttribute('aria-hidden', 'true'); toggle.setAttribute('aria-expanded', 'false'); document.body.classList.remove('menu-open-fixed'); window.scrollTo(0, scrollY); };
    toggle.addEventListener('click', () => drawer.classList.contains('open') ? cerrar() : abrir());
    overlay?.addEventListener('click', cerrar); closeBtn?.addEventListener('click', cerrar);
    $$('.drawer-link').forEach(a => a.addEventListener('click', cerrar));
    window.addEventListener('keydown', e => { if (e.key === 'Escape' && drawer.classList.contains('open')) cerrar(); });
    window.matchMedia('(min-width: 981px)').addEventListener?.('change', e => { if (e.matches && drawer.classList.contains('open')) cerrar(); });
  }

  // ---- Índice de la guía: resalta el capítulo que está bajo la barra y responde al clic ----
  function guiaIndice() {
    const enlaces = $$('.guia-nav a'); if (!enlaces.length) return;
    const caps = enlaces.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const LIMITE = 140; // px bajo el borde superior (barra fija + margen)
    let fijado = null, fijadoHasta = 0;
    const marcar = (id) => enlaces.forEach(a => a.classList.toggle('activo', a.getAttribute('href') === '#' + id));
    const calcular = () => {
      if (fijado && performance.now() < fijadoHasta) { marcar(fijado); return; }
      let actual = caps[0];
      for (const c of caps) { if (c.getBoundingClientRect().top <= LIMITE) actual = c; }
      // al llegar al final de la página, el último capítulo
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) actual = caps[caps.length - 1];
      if (actual) marcar(actual.id);
    };
    let pendiente = false;
    const onScroll = () => { if (!pendiente) { pendiente = true; requestAnimationFrame(() => { pendiente = false; calcular(); }); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    enlaces.forEach(a => a.addEventListener('click', (e) => {
      const id = a.getAttribute('href').slice(1), destino = document.getElementById(id);
      if (!destino) return;
      e.preventDefault();
      fijado = id; fijadoHasta = performance.now() + 900; marcar(id);
      destino.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      history.replaceState(null, '', '#' + id);
      setTimeout(calcular, 950);
    }));
    calcular();
  }

  // ---- Fachada ligera de YouTube ----
  window.crearVideo = function (v, span, etiqueta) {
    const poster = v.id ? `https://i.ytimg.com/vi/${v.id}/maxresdefault.jpg` : (document.body.dataset.raiz || '') + 'images/web/consultorio2-1200.webp';
    const fig = document.createElement('figure');
    fig.className = `tile tile-video ${span} reveal` + (v.id ? '' : ' pendiente');
    fig.innerHTML = `
      <img src="${poster}" alt="" loading="lazy" decoding="async" ${v.id ? `onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/${v.id}/hqdefault.jpg'"` : ''} />
      <button class="video-play" type="button" aria-label="Reproducir: ${v.titulo}" ${v.id ? '' : 'disabled'}><i class="fa-solid fa-play" aria-hidden="true"></i></button>
      <figcaption class="video-pie"><span class="video-tema">${etiqueta}</span><strong>${v.titulo}</strong>${v.id ? '' : '<span class="video-nota">Próximamente</span>'}</figcaption>`;
    if (v.id) fig.querySelector('.video-play').addEventListener('click', () => {
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube-nocookie.com/embed/${v.id}?autoplay=1&rel=0`; iframe.title = v.titulo;
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; iframe.allowFullscreen = true;
      fig.classList.add('reproduciendo'); fig.appendChild(iframe);
    });
    return fig;
  };

  // ---- Arranque: lo específico de cada página corre antes (window.renderPagina) ----
  // ---- Precarga de marca: se retira cuando termina la animación y la página cargó ----
  (function precarga() {
    const el = document.getElementById('precarga'); if (!el) return;
    if (document.documentElement.classList.contains('sin-precarga')) { el.remove(); return; }
    const inicio = performance.now(), MINIMO = 2000, MAXIMO = 3500;
    let cargado = document.readyState === 'complete';
    window.addEventListener('load', () => { cargado = true; });
    const quitar = () => { el.classList.add('fuera'); try { sessionStorage.setItem('precarga', '1'); } catch (e) {} setTimeout(() => el.remove(), 700); };
    const revisar = () => {
      const t = performance.now() - inicio;
      if ((cargado && t >= MINIMO) || t >= MAXIMO) quitar(); else setTimeout(revisar, 100);
    };
    revisar();
  })();

  document.addEventListener('DOMContentLoaded', () => {
    if (typeof window.renderPagina === 'function') window.renderPagina();
    espaciosImagen();
    iconos();
    menu();
    contadores();
    guiaIndice();
    aparicion();
  });
})();
