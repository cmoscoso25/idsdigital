# FRONTEND.md — IDS Digital · Guía Visual Oficial

**Versión:** 2.0 · **Actualizado:** 2026-06-03
Fuente de verdad para toda tarea visual: UI, UX, HTML, CSS, JS, formularios, tablas, dashboards.
Leer este archivo SOLO cuando la tarea involucre diseño, frontend o componentes visuales.

---

## 1. Identidad visual corporativa

**Producto:** IDS Digital — plataforma SaaS B2B para empresas chilenas que contratan servicios de IA, automatización y desarrollo.
**Posicionamiento visual:** tecnología de confianza · precisión operativa · formalidad sin frialdad.

### Paleta

La paleta canónica está definida en `static/css/styles.css` (CRM) y `static/css/public.css` (landing).
No inventar colores fuera de esa paleta. Referencia de roles:

| Rol | Uso |
|---|---|
| Color primario | Acciones principales, CTA, enlaces activos, indicadores de foco |
| Color secundario | Acentos, badges de estado, hover secundario |
| Fondo base | Blanco o gris muy claro — nunca fondos de color intenso en el cuerpo |
| Fondo panel | Gris claro neutro para sidebars, headers de sección, zebra de tablas |
| Texto principal | Casi negro — nunca gris demasiado claro en texto informativo |
| Texto secundario | Gris medio — metadatos, labels, marcas de tiempo |
| Alerta / error | Rojo — solo para errores y acciones destructivas |
| Éxito | Verde — solo para confirmaciones y estados positivos |
| Advertencia | Amarillo/naranja — solo para riesgos y estados pendientes |

### Tipografía

- Definida en los archivos CSS existentes. No agregar fuentes nuevas sin aprobación.
- Jerarquía: `h1` → título de página · `h2` → sección · `h3` → subsección o card header.
- Texto de cuerpo: tamaño legible sin zoom en 1366×768.
- Labels de formulario y cabeceras de tabla: peso medio (semibold), nunca italic.

### Iconografía

- Usar el set de íconos ya definido en el proyecto. No mezclar sets distintos.
- Íconos funcionales (acciones, estados): siempre acompañados de texto label o tooltip.
- Íconos decorativos: usar con moderación, solo si aportan orientación visual, no decoración vacía.

---

## 2. Filosofía de diseño

**Principio rector:** el diseño sirve al flujo de trabajo, no al revés.

| Principio | Aplicación concreta |
|---|---|
| Productividad primero | El CRM reduce clicks. El dato crítico está visible sin scroll. |
| Conversión directa | La landing lleva al formulario de demo sin fricción. |
| Claridad sobre creatividad | Si hay duda entre lo vistoso y lo claro, siempre lo claro. |
| Consistencia sobre originalidad | Un patrón nuevo requiere justificación. Un patrón existente se reutiliza. |
| Jerarquía visible | El usuario sabe en 2 segundos qué puede hacer y qué es lo más importante. |

NEVER: efectos decorativos sin propósito · animaciones que distraigan · información oculta en hover sin indicación · modales que bloqueen trabajo frecuente.

---

## 3. Dos superficies visuales

| Superficie | Archivo CSS | Rutas | Audiencia |
|---|---|---|---|
| Landing pública | `static/css/public.css` | `/`, `/blog/`, `/servicios/`, `/automatizacion-procesos/`, `/desarrollo-software-medida/`, `/inteligencia-artificial-empresas/` | Prospectos B2B |
| CRM interno | `static/css/styles.css` | `/panel/*`, `/accounts/*` | Usuarios internos con rol RBAC |
| Chatbot | `static/css/diagnostico_ia.css` | `/agente-ia/` | Visitantes y usuarios |

MUST mantener paleta compartida y coherencia tipográfica entre superficies.
NEVER introducir estilos que funcionen en una superficie y rompan las otras.
NEVER editar `staticfiles/` — es generado por `collectstatic`.

---

## 4. UX — Landing pública

**Objetivo:** convertir visitantes B2B en solicitudes de demo (DemoRequest).

### Reglas de página

- CTA principal ("Solicitar demo" o equivalente) visible sin scroll en 1366×768.
- Propuesta de valor en los primeros 200px verticales.
- Secciones en orden: hero → beneficios → servicios → prueba social / casos → CTA final.
- Formulario de demo: mínimo campos posibles (nombre, empresa, email, teléfono). Sin campos opcionales visibles inicialmente.

### Navegación pública

- Header fijo con logo + links de navegación + botón CTA destacado.
- En mobile: menú hamburguesa, CTA siempre visible.
- Footer: links de secciones, datos de contacto, redes. Sin elementos de navegación secundaria redundantes.

### Páginas SEO (`/automatizacion-procesos/`, `/desarrollo-software-medida/`, `/inteligencia-artificial-empresas/`)

- Estructura: H1 con keyword → descripción del servicio → beneficios → CTA.
- No agregar elementos que diluyan el keyword principal.
- Breadcrumb solo si la jerarquía de contenido lo justifica.

---

## 5. UX — CRM interno (`/panel/*`)

**Objetivo:** que el equipo comercial gestione leads y solicitudes de demo con mínima fricción.

### Layout base

- Sidebar de navegación fija a la izquierda (colapsable en mobile).
- Contenido principal a la derecha del sidebar.
- Header de página con: título de sección · breadcrumb si hay más de un nivel · acciones rápidas a la derecha.
- NEVER usar tabs anidados más de un nivel de profundidad.

### Navegación CRM

| Ítem sidebar | Ruta | Rol mínimo |
|---|---|---|
| Solicitudes | `/panel/solicitudes/` | readonly |
| Leads | `/panel/leads/` | readonly |
| Agente IA | `/agente-ia/` | readonly |
| Admin Django | `/admin/` | admin |

- Ítem activo: indicador visual claro (fondo, borde lateral o color diferenciado).
- Rol del usuario visible en el header o sidebar (badge discreto).
- Logout: siempre accesible desde el header, acción POST (ya implementado).

### Flujo crítico: Solicitud → Lead

1. Lista de solicitudes (`/panel/solicitudes/`) → fila clickeable → detalle.
2. Detalle solicitud: información completa + botones de acción (Convertir / Archivar).
3. Convertir: modal de confirmación → redirige a detalle del lead creado.
4. Los estados de solicitud deben ser visualmente distinguibles (badges de color por estado).

---

## 6. Dashboards y KPIs

### Estructura de dashboard

```
[ KPI 1 ]  [ KPI 2 ]  [ KPI 3 ]  [ KPI 4 ]    ← fila superior, visible sin scroll
─────────────────────────────────────────────
[ Tabla principal / lista de registros       ]
[ Filtros inline o panel lateral de filtros  ]
```

- Máximo 4 KPIs en la primera fila visible.
- KPIs secundarios: debajo de la fila principal o en sección colapsable.
- NEVER gráficos decorativos sin datos reales — preferir métricas numéricas limpias.

### Diseño de KPI card

```
┌─────────────────────┐
│  Ícono  Etiqueta    │
│  Valor grande       │
│  Variación / sub    │
└─────────────────────┘
```

- Valor: tipografía grande, peso bold, color primario o neutro según contexto.
- Etiqueta: texto secundario pequeño, arriba o debajo del valor.
- Variación (subida/bajada): color verde/rojo + ícono de flecha. Solo si hay dato comparativo real.
- Hover: sombra suave o fondo levemente diferenciado. Sin tooltip vacío.

---

## 7. Tablas

### Estructura

- Cabecera: fondo diferenciado, texto semibold, no italic.
- Filas: zebra sutil (fila par levemente gris) O separadores horizontales — nunca ambos.
- Columna de acciones: alineada a la derecha, íconos o botones pequeños.
- Fila clickeable: cursor pointer + hover destacado si lleva a detalle.

### Contenido

- Columnas de fecha: formato `DD/MM/YYYY` o relativo (`hace 2 días`) — consistente en todo el proyecto.
- Columnas de estado: badge de color (pill/chip), no texto plano.
- Columnas largas (nombre, descripción): truncar con ellipsis + tooltip con valor completo.
- NEVER más de 7 columnas visibles simultáneamente en 1366px sin scroll horizontal interno.

### Estados especiales

- **Lista vacía:** mensaje útil + icono + acción sugerida. NEVER tabla vacía sin contexto.
- **Cargando:** skeleton loader o spinner centrado. NEVER pantalla en blanco.
- **Error de carga:** mensaje de error + botón de reintento.

### Paginación

- Sin paginación para listas <20 registros.
- Para listas largas: paginación simple (anterior / página actual / siguiente) — no paginación numérica compleja si no hay más de 5 páginas.

---

## 8. Formularios

### Layout

- Labels siempre visibles arriba del campo — NEVER solo placeholder como label.
- Un campo por fila en mobile. Máximo dos columnas en desktop para campos relacionados (ej: nombre + apellido).
- Sección de campos agrupada con separador visual si hay más de 6 campos.
- Botón submit: al final del formulario, alineado a la derecha o centrado según contexto. Nunca flotante sin justificación.

### Estados de campo

| Estado | Visual |
|---|---|
| Default | Borde gris neutro |
| Focus | Borde color primario + sombra suave |
| Error | Borde rojo + mensaje de error debajo del campo |
| Disabled | Opacidad reducida, cursor not-allowed |
| Éxito (opcional) | Borde verde + ícono check |

- Mensaje de error: inline, debajo del campo afectado. NEVER solo en el tope del formulario.
- Validación: preferir validación en blur (al salir del campo), no solo en submit.

### Formularios críticos del proyecto

| Formulario | Ruta | Campos clave |
|---|---|---|
| Solicitud de demo | `/` (landing) | nombre, empresa, email, teléfono |
| Login CRM | `/accounts/login/` | email o username, password |
| Convertir solicitud a lead | `/panel/solicitudes/<id>/convertir/` | modal de confirmación |
| Cambio de estado lead | `/panel/leads/<id>/estado/` | select de estado (POST) |

---

## 9. Modales

### Cuándo usar modal

- Confirmación de acción destructiva o irreversible (archivar, eliminar, convertir).
- Formulario corto que no justifica página propia (<4 campos).
- Vista previa de contenido sin salir del contexto actual.
- NEVER para contenido largo, flujos multi-paso complejos o información que el usuario necesita consultar frecuentemente.

### Estructura de modal

```
┌─────────────────────────────────┐
│ Título de la acción         [×] │
├─────────────────────────────────┤
│ Mensaje de confirmación o       │
│ campos del formulario           │
├─────────────────────────────────┤
│              [Cancelar] [Acción]│
└─────────────────────────────────┘
```

- Overlay: fondo semitransparente oscuro.
- Cierre: botón [×] en esquina superior derecha + click fuera del modal + tecla Esc.
- Botón de acción: color según tipo (primario para confirmar, rojo para destructivo).
- Botón cancelar: siempre presente, a la izquierda del botón de acción.
- Ancho: máximo 560px en desktop. En mobile: full width con margen lateral.
- NEVER scroll interno en modal salvo listas de selección muy largas.

---

## 10. Filtros

### Patrones permitidos

| Patrón | Cuándo usar |
|---|---|
| Filtros inline sobre la tabla | Listas simples con 1-3 filtros (ej: estado, fecha) |
| Panel lateral colapsable | Listas con 4+ filtros o combinaciones complejas |
| Barra de búsqueda + filtros secundarios | Cuando la búsqueda por texto es la acción primaria |

### Reglas

- El estado activo de los filtros debe ser visible en todo momento (badge de filtros aplicados o campos con valor).
- Botón "Limpiar filtros" visible cuando hay filtros activos.
- Los filtros no requieren botón "Aplicar" si se ejecutan en tiempo real (onChange). Si son lentos o costosos, usar botón "Filtrar" explícito.
- En mobile: filtros en panel deslizable (drawer) desde abajo o desde la derecha.

### Filtros del CRM (referencia)

- Lista de solicitudes: por estado (nuevo/contactado/descartado), por fecha.
- Lista de leads: por estado (nuevo/en_gestión/cotizado/cerrado/perdido), por responsable.

---

## 11. Responsive y resoluciones

### Breakpoints

| Breakpoint | Ancho | Contexto |
|---|---|---|
| Mobile | <768px | Smartphones |
| Tablet | 768px – 1024px | Tablets, algunos notebooks |
| **Notebook (primario)** | **1024px – 1366px** | **Target principal CRM** |
| Desktop | >1366px | Monitores externos |

### Reglas por superficie

**Landing pública:**
- Mobile-first. El formulario de demo debe ser usable con una mano en mobile.
- Hero y CTA visibles sin scroll en todos los breakpoints.
- Imágenes y videos: `max-width: 100%`, nunca overflow horizontal.

**CRM interno:**
- Sidebar colapsada en <1024px (icono only o drawer).
- Tablas: scroll horizontal interno dentro del contenedor — NEVER romper layout de página.
- KPIs: de 4 columnas en desktop a 2 en tablet a 1 en mobile.
- Formularios: de 2 columnas en desktop a 1 en mobile.

### Verificación obligatoria

Antes de entregar cualquier cambio visual, verificar:
- [ ] Sin scroll horizontal en 1366×768.
- [ ] Contenido crítico visible sin scroll vertical en 1366×768.
- [ ] Tabla funcional (scroll interno) en mobile.
- [ ] Formulario usable en mobile.
- [ ] Modal funcional en mobile (full width).

---

## 12. Consistencia entre módulos

### Patrones de reutilización obligatoria

Todo módulo nuevo del CRM MUST seguir estos patrones ya establecidos:

| Patrón | Descripción |
|---|---|
| Header de página | Título H1 + breadcrumb + acciones a la derecha |
| Lista con filtros | Filtros arriba de la tabla + estado vacío definido |
| Detalle de registro | Card con datos + sección de acciones + historial/notas si aplica |
| Confirmación de acción | Modal con mensaje + botones Cancelar / Confirmar |
| Feedback de acción | Toast o mensaje inline de éxito/error tras cada acción POST |
| Badge de estado | Pill de color por estado — paleta de estados definida globalmente |

### Paleta de estados (badges) — CRM

| Estado | Color semántico |
|---|---|
| Nuevo | Azul / primario |
| En gestión | Amarillo / advertencia |
| Cotizado | Naranja |
| Cerrado (ganado) | Verde |
| Perdido / Descartado | Gris o rojo suave |
| Contactado | Azul claro |

MUST usar el mismo color para el mismo estado en solicitudes y leads.

---

## 13. Criterios para futuras páginas

Antes de diseñar o implementar una nueva página o sección, responder:

1. **¿A qué superficie pertenece?** Landing pública → `public.css`. CRM → `styles.css`.
2. **¿Qué patrón existente reutiliza?** Lista, detalle, formulario, dashboard. Documentar si introduce uno nuevo.
3. **¿El contenido crítico es visible sin scroll en 1366×768?** Si no, rediseñar jerarquía.
4. **¿Usa solo los componentes definidos en esta guía?** Cards, tablas, formularios, modales, filtros, KPIs.
5. **¿Mantiene coherencia con el módulo más similar ya implementado?** Revisar solicitudes o leads como referencia.
6. **¿El estado vacío, de carga y de error están definidos?** Toda lista y todo formulario necesita los tres.

### Páginas de referencia canónica

| Tipo | Referencia canónica en el proyecto |
|---|---|
| Lista con tabla y filtros | `/panel/solicitudes/` |
| Detalle de registro con acciones | `/panel/solicitudes/<id>/` |
| Lista de leads con estados | `/panel/leads/` |
| Formulario público de conversión | Landing (formulario de demo) |
| Login | `/accounts/login/` |

---

## 15. Animaciones — reglas y patrones establecidos

### Sistema de animación del hero (patrón canónico)

El hero de la landing usa **dos capas de animación independientes**:

| Capa | Técnica | Propósito |
|---|---|---|
| Canvas (JS) | `requestAnimationFrame` + partículas en red | Movimiento continuo, profundidad tecnológica |
| Aurora orbs (CSS) | `@keyframes` + `filter:blur` | Gradientes de color que se desplazan suavemente |
| Grid overlay (CSS) | `background-position` animado | Sensación de espacio infinito |
| Scan line (CSS) | `@keyframes scan` con `top` | Efecto terminal/tech sutil |

### Reglas de animación

- MUST respetar `prefers-reduced-motion` — el canvas comprueba antes de arrancar.
- MUST pausar el canvas con `IntersectionObserver` cuando el hero sale del viewport.
- NEVER usar videos, GIFs pesados ni librerías de animación externas.
- NEVER animar propiedades que activan layout (width, height, top, left). Solo `transform` y `opacity`.
- Duración de aurora orbs: 16–26s (`ease-in-out`) — percepción suave, no mecánica.
- Canvas: velocidad de partículas ≤ 0.35px/frame para elegancia.

### Reveal on scroll (patrón canónico)

```css
[data-reveal] {
  opacity: 0;
  transform: translateY(26px);
  transition: opacity 0.65s cubic-bezier(.22,.61,.36,1),
              transform 0.65s cubic-bezier(.22,.61,.36,1);
}
[data-reveal].revealed { opacity: 1; transform: translateY(0); }
```

```javascript
/* IntersectionObserver activa .revealed — zero libraries */
var obs = new IntersectionObserver(fn, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });
```

- `transition-delay` inline para stagger entre elementos hermanos (ej: `0.1s`, `0.15s`).
- Solo aplicar a elementos de sección — NEVER a elementos del hero (ya están en viewport).

### Tipografía — Inter (establecida en landing)

- Fuente: **Inter** desde Google Fonts CDN (400, 500, 600, 700, 800).
- `font-feature-settings: "cv02","cv03","cv04","cv11"` en `.landing-page`.
- `-webkit-font-smoothing: antialiased` en el body global.
- H1 landing: 52px / weight 800 / letter-spacing -0.04em.
- Section titles: 34px / weight 800 / letter-spacing -0.03em.

## 14. Archivos CSS — reglas de edición

| Archivo | Alcance | Regla |
|---|---|---|
| `static/css/styles.css` | CRM interno (`/panel/*`, `/accounts/*`) | Solo estilos de panel |
| `static/css/public.css` | Landing y páginas públicas | Solo estilos públicos |
| `static/css/diagnostico_ia.css` | Chatbot agente IA | Solo estilos del chatbot |

- NEVER mezclar estilos entre archivos de contextos distintos.
- NEVER usar `!important` salvo override de librería de terceros, con comentario que explique el motivo.
- NEVER hardcodear colores si ya existen como custom properties CSS.
- NEVER agregar librerías CSS externas (Bootstrap, Tailwind, Bulma) sin aprobación explícita.
- NEVER agregar librerías JS pesadas (jQuery, React, Vue) para funcionalidades que Django ya resuelve.
- NEVER introducir animaciones que degraden rendimiento en notebooks de gama media.
- NEVER editar `staticfiles/` — es generado por `collectstatic`.
