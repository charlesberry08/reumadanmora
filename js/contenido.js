/* Contenido configurable del sitio (redes, videos, podcast) y render de esas secciones */
  // =====================================================================
  //  CONFIGURACIÓN DE CONTENIDO (llenar con los datos reales del doctor)
  // =====================================================================
  // Redes: pegar la URL completa del perfil. Si se deja vacía, la tarjeta
  // se muestra sin liga (y la del pie de página se oculta).
  const REDES = {
    instagram: { url: 'https://www.instagram.com/reumatologodanielmora', usuario: '@reumatologodanielmora' },
    facebook:  { url: '', usuario: '' },
    tiktok:    { url: '', usuario: '' },
    youtube:   { url: 'https://www.youtube.com/@articulacionsonora1860', usuario: '@articulacionsonora1860' }
  };
  // Videos: "id" es el identificador del video en YouTube (lo que va después
  // de v= en la liga). Con id vacío se muestra la portada sin reproducir.
  // Los títulos son temas sugeridos; cambiarlos por los de los videos reales.
  const VIDEOS = [
    { id: 'lKNq-FuYCRQ', titulo: 'Conoce al Dr. Daniel Mora', tema: 'Presentación · Médica Campestre', grande: true },
    { id: '', titulo: '¿Cuándo acudir con un reumatólogo?', tema: 'Señales de alerta' },
    { id: '', titulo: 'Qué esperar en tu primera consulta', tema: 'La consulta' }
  ];
  // Podcast del doctor: canal, descripción y episodios (del más reciente al más antiguo).
  const PODCAST = {
    nombre: 'Articulación Sonora',
    url: 'https://www.youtube.com/@articulacionsonora1860',
    portada: 'images/web/podcast-articulacion-sonora-600.webp',
    descripcion: 'Podcast para la difusión de información sobre enfermedades reumáticas, dirigido al público en general. Contenidos y producción a cargo del Dr. Daniel Mora.',
    episodios: [
      { id: 'mNg73mhSi84', numero: 5, titulo: 'Tú puedes necesitar un reumatólogo: escucha y averígualo' },
      { id: 'Tw666pxnJHQ', numero: 4, titulo: 'Necesidades no cumplidas: acondicionamiento físico' },
      { id: '5ZIemNDB3bA', numero: 3, titulo: 'Necesidades no cumplidas: complejidad diagnóstica' },
      { id: 'rAE9PpOspxA', numero: 2, titulo: 'Fármacos' },
      { id: '5yswlgOP-7I', numero: 1, titulo: 'Necesidades no cumplidas: teorías' }
    ]
  };
  // =====================================================================

  const REDES_META = {
    instagram: { nombre: 'Instagram', icono: 'fa-brands fa-instagram', texto: 'Historias, consejos y avisos del consultorio.' },
    facebook:  { nombre: 'Facebook',  icono: 'fa-brands fa-facebook-f', texto: 'Publicaciones de divulgación y comunidad.' },
    tiktok:    { nombre: 'TikTok',    icono: 'fa-brands fa-tiktok', texto: 'Videos cortos con respuestas rápidas.' },
    youtube:   { nombre: 'YouTube',   icono: 'fa-brands fa-youtube', texto: 'Articulación Sonora, el podcast del doctor sobre enfermedades reumáticas.' }
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
    // Podcast
    const pg = $('#podcast-grid');
    if (pg) {
      const canal = document.createElement('a');
      canal.className = 'tile tile-marca podcast-canal c-5 r-2 reveal';
      canal.href = PODCAST.url; canal.target = '_blank'; canal.rel = 'noopener noreferrer';
      canal.innerHTML = `<img src="${PODCAST.portada}" alt="Portada de ${PODCAST.nombre}" width="400" height="400" loading="lazy" decoding="async" /><span class="etiqueta">Podcast del doctor</span><h3>${PODCAST.nombre}</h3><p>${PODCAST.descripcion}</p><span class="podcast-datos"><i class="fa-solid fa-headphones" aria-hidden="true"></i> ${PODCAST.episodios.length} episodios · YouTube</span><span class="btn btn-blanco"><i class="fa-brands fa-youtube" aria-hidden="true"></i> Ver el canal</span>`;
      pg.appendChild(canal);
      PODCAST.episodios.forEach((e, i) => pg.appendChild(crearVideo(e, i === 0 ? 'c-7 r-2 grande' : 'c-3', `Episodio ${String(e.numero).padStart(2, '0')}`)));
    }
  };
