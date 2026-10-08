/* Contenido configurable del sitio (redes y videos) y render de esas secciones */
  // =====================================================================
  //  CONFIGURACIÓN DE CONTENIDO (llenar con los datos reales del doctor)
  // =====================================================================
  // Redes: pegar la URL completa del perfil. Si se deja vacía, la tarjeta
  // se muestra sin liga (y la del pie de página se oculta).
  const REDES = {
    instagram: { url: 'https://www.instagram.com/reumatologodanielmora', usuario: '@reumatologodanielmora' },
    facebook:  { url: '', usuario: '' },
    tiktok:    { url: '', usuario: '' },
    youtube:   { url: '', usuario: '' }
  };
  // Videos: "id" es el identificador del video en YouTube (lo que va después
  // de v= en la liga). Con id vacío se muestra la portada sin reproducir.
  // Los títulos son temas sugeridos; cambiarlos por los de los videos reales.
  const VIDEOS = [
    { id: 'lKNq-FuYCRQ', titulo: 'Conoce al Dr. Daniel Mora', tema: 'Presentación · Médica Campestre', grande: true },
    { id: '', titulo: '¿Cuándo acudir con un reumatólogo?', tema: 'Señales de alerta' },
    { id: '', titulo: 'Qué esperar en tu primera consulta', tema: 'La consulta' }
  ];
  // =====================================================================

  const REDES_META = {
    instagram: { nombre: 'Instagram', icono: 'fa-brands fa-instagram', texto: 'Historias, consejos y avisos del consultorio.' },
    facebook:  { nombre: 'Facebook',  icono: 'fa-brands fa-facebook-f', texto: 'Publicaciones de divulgación y comunidad.' },
    tiktok:    { nombre: 'TikTok',    icono: 'fa-brands fa-tiktok', texto: 'Videos cortos con respuestas rápidas.' }
  };

  // Render propio de la portada; js/comun.js se encarga del resto (iconos, menú, imágenes, aparición).
  window.renderPagina = function () {
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    // Redes
    const grid = $('#redes-grid'), foot = $('#footer-redes');
    Object.entries(REDES_META).forEach(([clave, meta]) => {
      const cfg = REDES[clave] || {}, tiene = !!cfg.url;
      const a = document.createElement('a');
      a.className = `tile tile-red red-${clave} c-3 reveal` + (tiene ? '' : ' pendiente');
      a.href = tiene ? cfg.url : '#redes';
      if (tiene) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
      a.setAttribute('aria-label', `${meta.nombre}${cfg.usuario ? ' ' + cfg.usuario : ''}`);
      if (grid) { a.innerHTML = `<span class="ico"><i class="${meta.icono}" aria-hidden="true"></i></span><span class="red-nombre">${meta.nombre}</span><span class="red-usuario">${cfg.usuario || 'Perfil del doctor'}</span><span class="red-texto">${meta.texto}</span><span class="red-flecha"><i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></span>`;
      grid.appendChild(a); }
      if (tiene && foot) { const li = document.createElement('li'); li.innerHTML = `<a href="${cfg.url}" target="_blank" rel="noopener noreferrer" aria-label="${meta.nombre}"><i class="${meta.icono}" aria-hidden="true"></i></a>`; foot.appendChild(li); }
    });
    // Videos
    const vg = $('#videos-grid');
    if (vg) VIDEOS.forEach(v => vg.appendChild(crearVideo(v, v.grande ? 'c-7 r-2 grande' : 'c-5', v.tema)));
  };
