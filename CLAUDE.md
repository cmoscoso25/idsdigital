# CLAUDE.md — Inteligencia Digital (IDS Digital)

## Reglas permanentes

- No modificar código funcional sin aprobación explícita del usuario.
- No crear archivos nuevos salvo que se solicite explícitamente.
- No hacer commits, pushes ni operaciones destructivas sin confirmación.
- No añadir comentarios que expliquen qué hace el código; solo el "por qué" si no es obvio.
- No agregar manejo de errores para escenarios que no pueden ocurrir.
- No introducir abstracciones prematuras; tres líneas similares son preferibles a una abstracción innecesaria.

## Convenciones de código

- **Lenguaje:** Python 3.11 / Django 6.0.2
- **Idioma de variables/funciones:** español (nombres de campos, modelos, vistas) excepto donde Django lo exige en inglés.
- **Modelos:** cada campo con `help_text` para campos no obvios; índices definidos en `Meta.indexes`.
- **Vistas:** siempre función (`@login_required`) salvo Class-Based Views de auth ya existentes.
- **URLs:** siempre usar `app_name` + `name` para reverses; nunca hardcodear rutas.
- **Templates:** herencia de `base.html`; parciales en `templates/includes/`.
- **CSS:** un solo archivo `static/css/styles.css` para CRM; `static/css/public.css` para landing pública.
- **Sin mocks en tests:** usar base de datos real para evitar divergencias.

## Flujo obligatorio de trabajo optimizado

Ejecutar en este orden al inicio de cada sesión y antes de cualquier tarea:

1. Leer `CLAUDE.md`.
2. Leer `PROJECT_CONTEXT.md`.
3. Leer `PROJECT_RULES.md`.
4. Leer `FRONTEND.md` **solo si** la tarea involucra UI, UX, HTML, CSS, JavaScript, dashboards, formularios, tablas, componentes visuales o diseño.
5. Usar memoria existente antes de leer código.
6. Usar CodeGraph antes de abrir archivos completos.
7. Ejecutar:
   - `codegraph status` — verificar que el índice esté activo.
   - `codegraph index` — solo si el índice está desactualizado.
8. Localizar archivos y símbolos con `codegraph_search` / `codegraph_context` o búsquedas acotadas con Grep (excluyendo `venv/`).
9. Leer solo los archivos mínimos necesarios para la tarea.
10. Leer solo los rangos de líneas relevantes en archivos grandes.
11. Si la tarea no autoriza modificación directa: proponer cambios con justificación clara, mostrar diff, esperar aprobación explícita.
12. Aplicar únicamente la tarea solicitada — sin refactorizaciones ni mejoras no pedidas.
13. Actualizar `PROJECT_CONTEXT.md` si hubo cambios técnicos, funcionales o arquitectónicos.
14. Actualizar `FRONTEND.md` si hubo cambios visuales, de UX o de componentes.
15. Actualizar `PROJECT_RULES.md` si se consolida una nueva regla permanente del proyecto.

### Restricciones permanentes de ejecución

- NEVER leer el proyecto completo — solo los archivos estrictamente necesarios para la tarea.
- NEVER pedir archivos ya documentados en `CLAUDE.md`, `PROJECT_CONTEXT.md`, `PROJECT_RULES.md` o `FRONTEND.md` salvo necesidad técnica concreta y justificada.
- NEVER crear archivos nuevos salvo solicitud explícita del usuario.
- NEVER hacer refactorizaciones masivas no solicitadas.
- NEVER hacer commits ni push sin aprobación explícita.
- NEVER romper funcionalidades existentes.
- NEVER explorar: `venv/` · `staticfiles/` · `.git/` · `__pycache__/` · `node_modules/`.
- MUST mantener compatibilidad con Django 6.0.2 y Python 3.11.
- MUST mantener coherencia con la arquitectura multi-tenant existente.

## Restricciones técnicas

- Python 3.11 (definido en `runtime.txt`).
- Django 6.0.2 — no usar APIs deprecadas de versiones anteriores.
- Base de datos: SQLite en desarrollo, PostgreSQL (psycopg2-binary) en producción vía `DATABASE_URL`.
- Email: `console.EmailBackend` en local; **Resend** en producción (variable `RESEND_API_KEY`).
- Archivos estáticos: WhiteNoise + `CompressedManifestStaticFilesStorage`.
- Deploy: Render.com (gunicorn, variables de entorno).
- Auth: modelo custom `accounts.User` (AbstractUser). Backend: `EmailOrUsernameBackend`.
- Multi-tenant: aislamiento por `Workspace`; middleware `CurrentWorkspaceMiddleware` inyecta `request.workspace`.

## Estrategia de optimización de tokens

- Usar `codegraph_search` antes de `Read` completo para localizar símbolos.
- Nunca hacer Glob sin excluir `venv/`, `staticfiles/`, `.git/`, `__pycache__/`.
- En búsquedas de texto, usar `Grep` con patrón de exclusión de `venv`.
- Leer solo los rangos de líneas necesarios en archivos grandes.
- No re-leer archivos recién editados (Edit/Write confirman el cambio).

## Uso obligatorio de CodeGraph

Antes de cualquier exploración masiva, ejecutar:

```bash
codegraph status          # verificar índice
codegraph index           # re-indexar si hay cambios
```

Para preguntas estructurales usar las herramientas MCP `codegraph_*` si el servidor está operativo,
o `codegraph` CLI como fallback.

**Nota actual:** El servidor MCP de CodeGraph requiere `better-sqlite3` o `node-sqlite3-wasm` que
no están instalados en el entorno MCP. Usar siempre el CLI como fallback.

## Procedimiento para futuras modificaciones

1. Verificar índice con `codegraph status`.
2. Identificar símbolo/archivo con CodeGraph o Grep (excluyendo `venv/`).
3. Leer solo el fragmento relevante del archivo.
4. Proponer el cambio con justificación clara.
5. Aplicar solo tras aprobación explícita del usuario.
6. Actualizar `PROJECT_CONTEXT.md` si el cambio es estructural.

## Sub-SaaS: Nexa AI

- Ruta pública: `/nexa/` → vista `public.nexa` → template `templates/public/nexa.html`
- CSS landing: `static/css/nexa.css` (scoped bajo `.nexa-page`)
- **App Django `nexa`** implementada (MVP activo desde 2026-06-04):
  - Panel privado en `/nexa/app/` — todas las vistas con `@login_required`.
  - Modelos: `EmpresaNexa`, `MemoriaMarca`, `ContenidoGenerado`.
  - Servicio IA: `nexa/services/generador_contenido.py` (simulado, listo para API).
  - Templates en `templates/nexa/` — base con sidebar `base_nexa.html`.
  - CSS panel: `static/css/nexa_app.css` (scoped bajo `.nxa-app`).
  - No usar `Workspace` en Nexa aún — las empresas son FK a `accounts.User`.
- El formulario de demo de Nexa reutiliza `DemoRequest` con `necesidad = "Nexa AI — Demo anticipada"`.
- Pillow (12.2.0) requerido para `EmpresaNexa.logo` (ImageField) — ya instalado.
- **Arquitectura de agentes** en `nexa/services/agentes/`: `estratega.py`, `copywriter.py`, `disenador.py`, `analista.py`.
- **EstrategiaMensual**: modelo con calendario_json (4 semanas). Vistas en `/nexa/app/estrategias/`.
- **Visualizador de slides**: `contenido_detalle.html` renderiza `estructura_json` visualmente via JS; JSON oculto con toggle.
- **Producción automática**: `generar_contenido_mes` (POST `/nexa/app/estrategias/<id>/generar/`) itera el `calendario_json`, llama al copywriter por cada publicación y crea `ContenidoGenerado` vinculado a la estrategia.
- **Copywriter v3** (2026-06-04): `nexa/services/agentes/copywriter.py` genera contenido con estructura narrativa profesional por formato:
  - **Post**: Hook → Beneficio → Prueba/dato → CTA (`estructura_json.secciones` con 4 entradas)
  - **Historia**: 3 pantallas rol-diferenciadas: `problema` (¿te ha pasado? + encuesta) → `consecuencia` (costo de no actuar + deslizador) → `solucion` (marca + propuesta + link)
  - **Carrusel**: 6 slides obligatorios: portada → problema → `consecuencia` → `solucion` → beneficio → cta
  - **Reel**: 5 escenas con `texto_pantalla` (versión corta para on-screen) y `duracion_seg`: hook(5s) → problema(5s) → solucion(10s) → beneficio(5s) → cta(5s)
  - Nuevos helpers: `_prueba_post`, `_texto_problema_historia`, `_consecuencia_historia`, `_consecuencia_slide`, `_solucion_slide`, `_problema_reel`, `_solucion_reel`, `_beneficio_reel`
  - Render visual actualizado: tipos `consecuencia` (fondo rojo oscuro, ⚠️) y `solucion` (azul positivo, ✓) en carrusel; tipos `problema/solucion/beneficio` en reel.
- **Biblioteca**: filtros por empresa, estrategia, tipo y estado. KPIs: total, borradores, aprobados, programados, publicados.
- **Progress en estrategia**: planificados/generados/avance% calculados en vista, barra visual en template.
- **Creatividades Instagram** (2026-06-04): módulo completo en `nexa/`. Modelo `CreatividadInstagram` tiene `render_html` + `render_css` (campos server-side, listos para reemplazar por imagen IA real). Agente `agente_diseno_instagram.py` genera 4 renders HTML inline-styled: Post (1:1 con chrome Instagram), Historia (3 pantallas 9:16 con stickers), Carrusel (slides navegables con JS), Reel (storyboard 2 cols). Para conectar IA de imágenes: solo cambiar las funciones `_render_*` para devolver `<img src="url_api">` en lugar del HTML generado.
- `static/css/nexa_app.css` incluye estilos `.nxa-ig-*` para mockups de Instagram y `.nxar-kpi-*` para KPI cards.
- **Composición visual inteligente** (2026-06-04 v2): `agente_diseno_instagram.py` incluye 3 helpers de composición:
  - `_kpi_cards(categoria, c1)` → 3 KPI metrics por industria dentro del post.
  - `_slide_body(tipo, s, vis, c1, c2)` → contenido diferenciado por tipo de slide en carrusel (portada/problema/contenido/beneficio/cta).
  - `_escena_visual(tipo, vis, c1, c2, num)` → frames numerados estilo CapCut para reel.
  - Post: accent bar + KPI cards + CTA premium (fondo blanco con color de marca).
  - Historia: hero SVG de categoría en pantalla 0, progress bar + chip en pantalla 1, CTA button en pantalla 2.
- Próximo paso crítico: conectar agentes con Claude API (Anthropic SDK en requirements).

## Gestión de contexto — archivos de referencia

Leer siempre al inicio de cada sesión:
- `CLAUDE.md` — reglas permanentes, convenciones y restricciones técnicas.
- `PROJECT_CONTEXT.md` — arquitectura, modelos, URLs, estado actual del proyecto.

Leer solo si la tarea involucra HTML, CSS, JS, UX, UI, dashboards, formularios, tablas o diseño visual:
- `FRONTEND.md` — reglas visuales, componentes, restricciones de diseño.

MUST usar `codegraph_search` o `codegraph_context` antes de abrir archivos completos.
NEVER solicitar archivos ya documentados en estos tres archivos salvo necesidad técnica concreta y justificada.
NEVER explorar: `venv/` · `staticfiles/` · `.git/` · `__pycache__/` · `node_modules/`
