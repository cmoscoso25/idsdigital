# DESIGN_SYSTEM.md — IDS Digital · Sistema de Diseño Oficial

**Versión:** 1.0 · **Actualizado:** 2026-06-03
Sistema de diseño canónico para CRM, landing pública y módulos futuros.
Leer junto con `FRONTEND.md` en tareas visuales. Este archivo define el **qué**; `FRONTEND.md` define el **por qué** y el **cuándo**.

---

## 0. Tipografía oficial

**Fuente primaria:** Inter (Google Fonts CDN)
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
```

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
font-feature-settings: "cv02","cv03","cv04","cv11";
-webkit-font-smoothing: antialiased;
```

| Uso | Tamaño | Peso | Letter-spacing |
|---|---|---|---|
| H1 landing hero | 52px | 800 | -0.04em |
| Section title landing | 34px | 800 | -0.03em |
| H1 blog | 28px | 700 | -0.02em |
| Card title | 15px | 700 | -0.02em |
| Body | 15–16px | 400 | 0 |
| Label / meta | 11–13px | 500–600 | 0.01–0.11em |

## Principios base

| Prioridad | Principio |
|---|---|
| 1 | SaaS B2B premium — sin ruido visual, sin Bootstrap genérico |
| 2 | Productividad — el dato crítico visible sin scroll |
| 3 | Notebook 1366×768 como resolución objetivo primaria |
| 4 | Mínimo scroll — diseñar para el viewport, no para el desplazamiento |
| 5 | Máxima claridad — jerarquía obvia, acciones evidentes |

---

## 1. Colores

Los valores hex canónicos están definidos en `static/css/styles.css` (CRM) y `static/css/public.css` (landing).
No usar valores hex directamente en templates — solo clases utilitarias o custom properties CSS ya declaradas.

### Roles semánticos

| Token semántico | Uso |
|---|---|
| `--color-primary` | Acciones principales, CTA, bordes de focus, ítem de nav activo |
| `--color-primary-dark` | Hover del botón primario, encabezados de sección destacados |
| `--color-secondary` | Acentos, badges informativos, hover secundario |
| `--color-bg` | Fondo de página — blanco o gris muy claro |
| `--color-bg-panel` | Fondo de sidebar, cabeceras de card, filas zebra |
| `--color-bg-surface` | Fondo de cards, modales, formularios |
| `--color-text-primary` | Texto principal — contraste mínimo 4.5:1 sobre `--color-bg` |
| `--color-text-secondary` | Metadatos, labels, timestamps, texto de ayuda |
| `--color-text-disabled` | Campos deshabilitados, texto inactivo |
| `--color-border` | Bordes de cards, inputs, separadores de tabla |
| `--color-border-focus` | Igual a `--color-primary` — borde de input en estado focus |
| `--color-danger` | Errores, acciones destructivas, estado perdido/descartado |
| `--color-warning` | Advertencias, estado en gestión, cotizado |
| `--color-success` | Confirmaciones, estado cerrado/ganado |
| `--color-info` | Estado nuevo, información neutral |

### Paleta de estados (badges CRM)

| Estado | Token de color | Superficies que lo usan |
|---|---|---|
| Nuevo | `--color-info` | Solicitudes, Leads |
| Contactado | Azul claro / variante de info | Solicitudes |
| En gestión | `--color-warning` | Leads |
| Cotizado | Naranja / variante de warning | Leads |
| Cerrado (ganado) | `--color-success` | Leads |
| Perdido / Descartado | `--color-danger` suave o gris | Leads, Solicitudes |

MUST usar el mismo token para el mismo estado en todos los módulos.

---

## 2. Espaciados

Sistema de grilla de 4px. Todos los márgenes y paddings son múltiplos de 4.

| Token | Valor | Uso típico |
|---|---|---|
| `--space-1` | 4px | Separación mínima entre elementos inline |
| `--space-2` | 8px | Gap entre ícono y label, padding de badge |
| `--space-3` | 12px | Padding de botón compacto |
| `--space-4` | 16px | Padding estándar de card, input, celda de tabla |
| `--space-5` | 20px | Separación entre secciones dentro de una card |
| `--space-6` | 24px | Gap entre cards en una fila, margen de sección |
| `--space-8` | 32px | Separación entre bloques de sección mayores |
| `--space-10` | 40px | Margen de página en mobile |
| `--space-12` | 48px | Padding de sección en landing |
| `--space-16` | 64px | Separación entre secciones de landing |

### Reglas de separación entre bloques

- Entre KPIs y tabla principal: `--space-6`.
- Entre card y card en grid: `--space-6`.
- Entre label e input: `--space-2`.
- Entre campos de formulario: `--space-5`.
- Entre secciones de página CRM: `--space-8`.
- Entre secciones de landing: `--space-16`.
- Padding interno de página CRM: `--space-6` horizontal, `--space-6` vertical.

---

## 3. Cards

### Tamaños

| Tipo | Uso | Ancho |
|---|---|---|
| Card full | Contenedor principal de detalle o formulario | 100% del contenedor |
| Card 1/2 | Dos columnas en desktop | `calc(50% - var(--space-3))` |
| Card 1/3 | Tres columnas — KPIs, métricas | `calc(33.33% - var(--space-4))` |
| Card 1/4 | Cuatro columnas — KPIs en fila superior | `calc(25% - var(--space-4))` |

En mobile (< 768px): todas las cards en 100%.
En tablet (768–1024px): máximo 2 columnas.

### Bordes y sombras

```
border: 1px solid var(--color-border)
border-radius: 8px
background: var(--color-bg-surface)
box-shadow: 0 1px 3px rgba(0,0,0,0.07)
```

Hover (solo cards clickeables):
```
box-shadow: 0 4px 12px rgba(0,0,0,0.10)
transition: box-shadow 0.15s ease
```

NEVER: sombras gruesas, bordes dobles, border-radius > 12px en cards de datos.

### Espaciado interno

```
padding: var(--space-6)                    /* 24px — card estándar */
padding: var(--space-4)                    /* 16px — card compacta (KPI, sidebar) */
```

### Header de card

```
border-bottom: 1px solid var(--color-border)
padding-bottom: var(--space-4)
margin-bottom: var(--space-5)
font-weight: 600
```

---

## 4. Botones

### Variantes

| Variante | Uso | Estilo base |
|---|---|---|
| Primario | Acción principal de la página — solo uno por vista | Fondo `--color-primary`, texto blanco |
| Secundario | Acciones alternativas, filtros | Borde `--color-primary`, fondo transparente, texto `--color-primary` |
| Peligro | Archivar, eliminar, acciones destructivas | Fondo `--color-danger`, texto blanco |
| Éxito | Confirmar, guardar completado | Fondo `--color-success`, texto blanco |
| Ghost | Cancelar, cerrar modal | Sin borde, fondo transparente, texto `--color-text-secondary` |
| Ícono | Acción rápida en tabla o header | Solo ícono, sin label visible (con tooltip obligatorio) |

### Tamaños

| Tamaño | Alto | Padding horizontal | Uso |
|---|---|---|---|
| `sm` | 32px | 12px | Acciones en tabla, filtros compactos |
| `md` (default) | 40px | 20px | Acciones estándar de formularios y páginas |
| `lg` | 48px | 28px | CTA principal de landing |

### Estados

```
/* Default */
border-radius: 6px
font-weight: 500
transition: background 0.15s ease, box-shadow 0.15s ease

/* Hover — primario */
background: var(--color-primary-dark)
box-shadow: 0 2px 6px rgba(0,0,0,0.15)

/* Focus */
outline: 2px solid var(--color-primary)
outline-offset: 2px

/* Disabled */
opacity: 0.5
cursor: not-allowed
pointer-events: none

/* Loading */
cursor: wait
opacity: 0.8
[spinner inline antes del label]
```

### Reglas de uso

- NEVER dos botones primarios en la misma vista.
- NEVER tres botones del mismo peso visual en la misma fila.
- Botón destructivo: siempre acompañado de modal de confirmación.
- En mobile: botones de acción principal full width.

---

## 5. Formularios

### Labels

```
display: block
font-size: 14px
font-weight: 500
color: var(--color-text-primary)
margin-bottom: var(--space-2)    /* 8px — siempre visible, nunca solo placeholder */
```

### Inputs y Selects

```
width: 100%
height: 40px
padding: 0 var(--space-4)
border: 1px solid var(--color-border)
border-radius: 6px
font-size: 15px
color: var(--color-text-primary)
background: var(--color-bg-surface)
transition: border-color 0.15s ease, box-shadow 0.15s ease

/* Focus */
border-color: var(--color-border-focus)
box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.15)
outline: none

/* Error */
border-color: var(--color-danger)

/* Disabled */
opacity: 0.6
cursor: not-allowed
background: var(--color-bg-panel)
```

### Textarea

```
/* Igual que input + */
height: auto
min-height: 100px
padding: var(--space-3) var(--space-4)
resize: vertical
```

### Mensajes de validación

```
/* Error */
font-size: 13px
color: var(--color-danger)
margin-top: var(--space-1)
display: block

/* Ayuda */
font-size: 13px
color: var(--color-text-secondary)
margin-top: var(--space-1)
```

NEVER: mensaje de error solo en el tope del formulario. MUST: error inline debajo del campo afectado.

### Layout de formulario

```
/* Grid de campos */
display: grid
gap: var(--space-5)                              /* 20px entre campos */
grid-template-columns: 1fr                       /* mobile */
grid-template-columns: 1fr 1fr                   /* desktop — máximo 2 columnas */

/* Sección de acciones */
display: flex
justify-content: flex-end
gap: var(--space-3)
margin-top: var(--space-8)
padding-top: var(--space-5)
border-top: 1px solid var(--color-border)
```

---

## 6. KPIs

### Estructura de card KPI

```
┌──────────────────────────┐
│ [ícono 20px]  Etiqueta   │  ← fila superior: ícono + label (text-secondary, 13px)
│                          │
│ Valor grande             │  ← número principal (28–32px, font-weight: 700)
│                          │
│ ▲ +12% vs. mes anterior  │  ← variación (13px, color según sube/baja)
└──────────────────────────┘
```

### Tipografía KPI

| Elemento | Tamaño | Peso | Color |
|---|---|---|---|
| Valor principal | 28px (desktop) / 24px (tablet) | 700 | `--color-text-primary` |
| Etiqueta | 13px | 500 | `--color-text-secondary` |
| Variación positiva | 13px | 500 | `--color-success` |
| Variación negativa | 13px | 500 | `--color-danger` |
| Variación neutra | 13px | 400 | `--color-text-secondary` |

### Distribución

```
/* Fila de KPIs — desktop */
display: grid
grid-template-columns: repeat(4, 1fr)
gap: var(--space-6)

/* Tablet */
grid-template-columns: repeat(2, 1fr)

/* Mobile */
grid-template-columns: 1fr
```

- Máximo 4 KPIs en la fila superior visible sin scroll en 1366×768.
- KPIs secundarios: segunda fila o sección colapsable.
- NEVER gráficos decorativos sin datos reales.
- Ícono: 20px, mismo color que la etiqueta o ligeramente más claro.

---

## 7. Tablas

### Estructura

```html
<table>
  <thead>                          <!-- fondo: --color-bg-panel -->
    <tr>
      <th>Columna</th>             <!-- font-weight: 600, font-size: 13px, uppercase opcional -->
    </tr>
  </thead>
  <tbody>
    <tr class="fila-par">          <!-- background: var(--color-bg-panel) muy suave — zebra -->
    <tr class="fila-impar">        <!-- background: var(--color-bg-surface) -->
  </tbody>
</table>
```

### CSS base

```
th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  border-bottom: 2px solid var(--color-border);
}

td {
  padding: var(--space-3) var(--space-4);
  font-size: 14px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

tr:hover td {
  background: rgba(var(--color-primary-rgb), 0.04);
}

tr[data-href] { cursor: pointer; }       /* fila clickeable */
```

### Columna de acciones

```
text-align: right
white-space: nowrap
width: 1%                              /* colapsa al mínimo necesario */
```

### Truncado de texto largo

```
max-width: 200px
overflow: hidden
text-overflow: ellipsis
white-space: nowrap
```
Acompañar con `title` o tooltip con el valor completo.

### Responsive

```
/* Contenedor */
overflow-x: auto
-webkit-overflow-scrolling: touch
border-radius: 8px
border: 1px solid var(--color-border)
```

NEVER romper el layout de página con scroll horizontal de tabla.

### Paginación

```
display: flex
align-items: center
justify-content: space-between
padding: var(--space-4) var(--space-4)
border-top: 1px solid var(--color-border)
font-size: 14px
```

- Sin paginación para < 20 registros.
- Patrón: `← Anterior  |  Página 2 de 8  |  Siguiente →`
- En mobile: ocultar conteo de páginas, mantener solo flechas.

### Estados especiales de tabla

```
/* Lista vacía */
.empty-state {
  padding: var(--space-12) var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
}
/* Incluir: ícono descriptivo (48px) + título + mensaje + CTA opcional */

/* Cargando */
/* Skeleton loader: filas con fondo --color-bg-panel animado */

/* Error */
/* Mensaje de error + botón Reintentar */
```

---

## 8. Dashboards

### Layout recomendado

```
┌─────────────────────────────────────────────────────┐
│ SIDEBAR │ [Header de página: título + acciones]      │
│         ├─────────────────────────────────────────── │
│         │ [KPI] [KPI] [KPI] [KPI]    ← fila 1       │
│         │                                            │
│         │ [Filtros inline o barra de búsqueda]       │
│         │                                            │
│         │ [Tabla principal                         ] │
│         │ [                                        ] │
│         │ [Paginación                              ] │
└─────────────────────────────────────────────────────┘
```

### Orden de componentes

1. Header de página (título H1 + breadcrumb + acciones rápidas).
2. Fila de KPIs (máximo 4, visibles sin scroll).
3. Barra de filtros / búsqueda.
4. Tabla o lista principal.
5. Paginación.
6. Secciones secundarias (si aplica) — debajo del pliegue.

### Densidad de información

- Padding de página: `var(--space-6)` en todos los lados.
- Gap entre bloques verticales: `var(--space-6)`.
- NEVER más de 7 columnas en tabla sin scroll horizontal interno.
- NEVER texto de más de 2 líneas en celda de tabla sin truncado.
- NEVER secciones colapsadas por defecto si contienen información de uso frecuente.

### Header de página

```
display: flex
align-items: center
justify-content: space-between
margin-bottom: var(--space-6)
padding-bottom: var(--space-5)
border-bottom: 1px solid var(--color-border)

h1 {
  font-size: 22px;
  font-weight: 700;
}

.page-actions {
  display: flex;
  gap: var(--space-3);
}
```

---

## 9. Modales

### Tamaños

| Tamaño | Ancho máximo | Uso |
|---|---|---|
| `sm` | 400px | Confirmación simple (archivar, eliminar) |
| `md` (default) | 560px | Formulario corto (1–4 campos), detalle compacto |
| `lg` | 800px | Formulario largo, vista previa de contenido |

En mobile (< 768px): todos los tamaños = 100% de viewport con margen de 16px.

### Estructura

```
┌─────────────────────────────────────────────┐
│ Título de la acción                    [×]  │  ← header con borde inferior
├─────────────────────────────────────────────┤
│                                             │
│ Contenido: mensaje o campos de formulario   │
│                                             │
├─────────────────────────────────────────────┤
│                    [Ghost: Cancelar]  [CTA] │  ← footer con borde superior
└─────────────────────────────────────────────┘
```

### CSS base

```
/* Overlay */
background: rgba(0, 0, 0, 0.45)
backdrop-filter: blur(2px)

/* Contenedor */
border-radius: 10px
background: var(--color-bg-surface)
box-shadow: 0 20px 60px rgba(0,0,0,0.20)

/* Header */
padding: var(--space-5) var(--space-6)
border-bottom: 1px solid var(--color-border)
font-size: 17px
font-weight: 600

/* Body */
padding: var(--space-6)

/* Footer */
padding: var(--space-4) var(--space-6)
border-top: 1px solid var(--color-border)
display: flex
justify-content: flex-end
gap: var(--space-3)
```

### Comportamiento obligatorio

- Cierre con: botón [×] · click fuera del modal · tecla Escape.
- Foco atrapado dentro del modal mientras está abierto.
- NEVER scroll interno salvo listas de selección largas.
- NEVER modal para flujos multi-paso — usar páginas separadas.
- NEVER modal para información consultada frecuentemente.

---

## 10. Filtros

### Patrones y cuándo usar cada uno

| Patrón | Cuándo | Ejemplo en el proyecto |
|---|---|---|
| Filtros inline (sobre la tabla) | 1–3 filtros, sin combinaciones complejas | Estado de solicitud, fecha |
| Barra de búsqueda + chips | La búsqueda por texto es la acción primaria | Búsqueda de lead por nombre o email |
| Panel lateral colapsable | 4+ filtros o combinaciones complejas | Filtros avanzados de leads |
| Drawer (mobile) | Cualquier filtro en viewport < 768px | Versión mobile de cualquier filtro |

### Estructura de filtros inline

```
display: flex
align-items: center
gap: var(--space-3)
flex-wrap: wrap
margin-bottom: var(--space-4)
padding: var(--space-4)
background: var(--color-bg-panel)
border-radius: 8px
border: 1px solid var(--color-border)
```

### Comportamiento

- Filtros activos: siempre visibles — badge con conteo o campos con valor resaltado.
- "Limpiar filtros": botón ghost, visible solo cuando hay filtros activos.
- Aplicación: en tiempo real si la operación es rápida (onChange). Con botón "Filtrar" si hay latencia.
- En mobile: drawer deslizable desde abajo, con botón "Aplicar" y "Limpiar".

### CSS de chip de filtro activo

```
display: inline-flex
align-items: center
gap: var(--space-2)
padding: var(--space-1) var(--space-3)
background: rgba(var(--color-primary-rgb), 0.12)
color: var(--color-primary)
border-radius: 20px
font-size: 13px
font-weight: 500

.chip-close {
  cursor: pointer;
  opacity: 0.7;
}
.chip-close:hover { opacity: 1; }
```

---

## 11. Responsive

### Breakpoints

| Nombre | Rango | Comportamiento principal |
|---|---|---|
| Mobile | < 768px | 1 columna, sidebar como drawer, tablas con scroll |
| Tablet | 768–1023px | 2 columnas, sidebar colapsada (íconos) |
| **Notebook** | **1024–1366px** | **Target principal — sidebar + 2–4 columnas** |
| Desktop | > 1366px | Igual que notebook con más aire |

### Reglas por breakpoint — CRM

```css
/* Sidebar */
@media (max-width: 1023px) {
  .sidebar { width: 64px; }          /* íconos solo */
  .sidebar-label { display: none; }
}
@media (max-width: 767px) {
  .sidebar { transform: translateX(-100%); } /* drawer */
  .sidebar.open { transform: translateX(0); }
}

/* KPIs */
@media (max-width: 1023px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 767px)  { .kpi-grid { grid-template-columns: 1fr; } }

/* Formularios */
@media (max-width: 767px)  { .form-grid { grid-template-columns: 1fr; } }

/* Botones de acción */
@media (max-width: 767px)  { .action-primary { width: 100%; } }
```

### Reglas por breakpoint — Landing

```css
/* Hero */
@media (max-width: 767px) {
  .hero-title { font-size: 26px; }
  .hero-cta { width: 100%; text-align: center; }
}

/* Columnas de beneficios/servicios */
@media (max-width: 767px) { .features-grid { grid-template-columns: 1fr; } }
```

### Checklist de verificación responsive (obligatoria antes de entregar)

- [ ] Sin scroll horizontal en 1366×768.
- [ ] Contenido crítico visible sin scroll vertical en 1366×768.
- [ ] Tabla con scroll horizontal interno en mobile — NEVER rompe layout.
- [ ] Formulario usable con una mano en mobile (campos de 44px mínimo táctil).
- [ ] Modal funcional en mobile (full width, sin overflow).
- [ ] KPIs en una fila en notebook, en dos filas en tablet, en una columna en mobile.
- [ ] CTA de landing visible sin scroll en todos los breakpoints.

---

## 13. Animaciones — sistema canónico

### Keyframes establecidos (en `public.css`)

| Nombre | Duración | Uso |
|---|---|---|
| `aurora-1/2/3` | 18–26s ease-in-out | Orbs de fondo en hero |
| `grid-drift` | 40s linear | Grid overlay hero |
| `dot-pulse` | 2.5s ease-in-out | Badge live indicator |
| `btn-glow` | 4s ease-in-out | CTA button pulse |
| `border-shimmer` | 8s ease | Form card border gradient |
| `reveal-up` | 0.65s cubic-bezier | Fade-in on scroll |
| `badge-float` | 5s ease-in-out | Hero badge flotante |
| `scan` | 12s linear | Scan line decorativa del hero |

### Canvas de partículas — patrón canónico

```javascript
// Parámetros que NO deben cambiarse sin justificación:
var CONNECT = 155;                    // distancia máxima de conexión (px)
var MAX_PARTICLES = 55;               // cap de partículas (performance)
var PARTICLE_SPEED = 0.32;            // velocidad máxima por frame
var COLORS = ['#3b82f6','#6366f1','#8b5cf6','#06b6d4'];  // paleta oficial
```

- El canvas se pausa con `IntersectionObserver` cuando el hero sale del viewport.
- Las partículas hacen wrap (no bounce) para movimiento más fluido.
- El glow de cada partícula usa `createRadialGradient` con radio 5× el núcleo.

### Reglas

- NEVER animar `width`, `height`, `top`, `left`, `margin` — solo `transform` y `opacity`.
- NEVER usar `setInterval` para animaciones — solo `requestAnimationFrame`.
- MUST verificar `prefers-reduced-motion` antes de iniciar cualquier animación JS.
- NEVER cargar librerías de animación (GSAP, Framer, Anime.js) para efectos que CSS puede resolver.

## 12. Consistencia visual

### Patrones obligatorios en todos los módulos

Cada módulo nuevo MUST implementar estos patrones exactamente como los módulos existentes:

| Patrón | Especificación |
|---|---|
| Header de página | `h1` (22px, 700) + breadcrumb + `.page-actions` flex a la derecha |
| Badge de estado | Pill con `--color-{estado}`, 13px, padding 2px 10px, border-radius 20px |
| Estado vacío | Ícono 48px + título + mensaje descriptivo + CTA opcional, centrado |
| Feedback de acción POST | Toast o mensaje inline — éxito (verde) o error (rojo), auto-dismiss 4s |
| Confirmación destructiva | Modal `sm` con mensaje + botón Ghost (Cancelar) + botón Peligro |
| Fila de tabla clickeable | `data-href` o `cursor: pointer` + hover con fondo primario al 4% |

### Tokens CSS obligatorios

Todo componente nuevo MUST usar solo custom properties CSS — NEVER valores hardcodeados:

```css
/* ✓ Correcto */
color: var(--color-text-primary);
border: 1px solid var(--color-border);

/* ✗ Incorrecto */
color: #1a1a2e;
border: 1px solid #e2e8f0;
```

### Checklist de consistencia (antes de entregar cualquier componente nuevo)

- [ ] ¿Usa los tokens de color definidos en esta guía?
- [ ] ¿Usa el sistema de espaciados de 4px?
- [ ] ¿El border-radius es 6–8px (componentes) o 20px (pills/badges)?
- [ ] ¿El badge de estado usa la paleta definida en la sección de Colores?
- [ ] ¿El botón primario es el único de ese peso en la vista?
- [ ] ¿El estado vacío, de carga y de error están implementados?
- [ ] ¿El componente es funcional en 1366×768 sin scroll horizontal?
- [ ] ¿El hover y el focus tienen transición (0.15s ease)?
- [ ] ¿Se reutilizó un patrón existente en lugar de crear uno nuevo?

### Referencia de módulos canónicos

| Patrón a reutilizar | Módulo de referencia |
|---|---|
| Lista con tabla, filtros y estado vacío | `/panel/solicitudes/` |
| Detalle con acciones y notas | `/panel/solicitudes/<id>/` |
| Lista con badges de estado | `/panel/leads/` |
| Formulario público con CTA | Landing — formulario de demo |
| Login con campo email/password | `/accounts/login/` |
| Modal de confirmación | Convertir solicitud → Lead |
