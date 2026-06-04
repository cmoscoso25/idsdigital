# PROJECT_RULES.md — IDS Digital · Reglas permanentes

**Versión:** 1.0 · **Actualizado:** 2026-06-03
Decisiones permanentes del proyecto. Leer este archivo al inicio de cada sesión junto con CLAUDE.md y PROJECT_CONTEXT.md.
Objetivo: eliminar preguntas repetitivas y reducir consumo de tokens.

---

## 1. Qué archivo leer y cuándo

| Archivo | Leer cuando |
|---|---|
| `CLAUDE.md` | Siempre — reglas de comportamiento y convenciones de código |
| `PROJECT_CONTEXT.md` | Siempre — arquitectura, modelos, URLs, estado actual |
| `PROJECT_RULES.md` | Siempre — decisiones permanentes y restricciones transversales |
| `FRONTEND.md` | Solo si la tarea involucra HTML, CSS, JS, UX, UI, formularios, tablas o dashboards |

NEVER leer `venv/`, `staticfiles/`, `.git/`, `__pycache__/`, `node_modules/`.
NEVER leer archivos ya cubiertos en estos cuatro documentos salvo necesidad técnica concreta y justificada.
MUST usar `codegraph_search` o `codegraph_context` antes de abrir archivos completos.

---

## 2. Stack — decisiones bloqueadas

| Decisión | Valor | Por qué es permanente |
|---|---|---|
| Lenguaje | Python 3.11 | Definido en `runtime.txt` |
| Framework | Django 6.0.2 | No usar APIs de versiones anteriores |
| Base de datos dev | SQLite | Sin configuración extra local |
| Base de datos prod | PostgreSQL vía `DATABASE_URL` | Render.com |
| Email local | `console.EmailBackend` | Sin costo ni configuración |
| Email producción | Resend (`RESEND_API_KEY`) | Ya integrado |
| Archivos estáticos | WhiteNoise + `CompressedManifestStaticFilesStorage` | Sin S3/CDN |
| Deploy | Render.com + gunicorn | No cambiar sin decisión explícita |
| Auth | `accounts.User` (AbstractUser) + `EmailOrUsernameBackend` | Ya en producción |
| Multi-tenancy | `Workspace` + `CurrentWorkspaceMiddleware` | Arquitectura central del producto |

---

## 3. Arquitectura — decisiones permanentes

### Multi-tenancy
- Toda vista del CRM MUST filtrar por `request.workspace`.
- NEVER usar `Model.objects.all()` sin filtro de workspace en vistas del panel.
- `CurrentWorkspaceMiddleware` inyecta `request.workspace` desde `current_workspace_id` en sesión.
- El usuario selecciona workspace en `/accounts/workspace/` tras el login.

### Auth y roles
- Roles disponibles: `admin` · `supervisor` · `sales` · `readonly` (definidos en `accounts.Membership`).
- Login acepta email o username (`EmailOrUsernameBackend`).
- Logout: siempre POST — NEVER GET para logout.
- Vistas del panel: siempre decoradas con `@login_required`.
- Class-Based Views de auth: las ya existentes en `accounts` — no reemplazar por funciones.

### URLs
- ALWAYS usar `app_name` + `name` para reverses. NEVER hardcodear rutas.
- Namespace del panel CRM: rutas bajo `/panel/`.
- Namespace de cuentas: rutas bajo `/accounts/`.

### Modelos — reglas de campo
- Cada campo no obvio MUST tener `help_text`.
- Índices definidos en `Meta.indexes`, no como `db_index=True` en el campo.
- Constraint único de lead: `(workspace, email)` — no crear duplicados por workspace.

---

## 4. Convenciones de código — permanentes

| Aspecto | Regla |
|---|---|
| Idioma de variables | Español (campos, modelos, vistas, URLs) salvo donde Django exige inglés |
| Vistas | Siempre función con `@login_required` — excepto CBVs de auth existentes |
| Templates | Herencia de `base.html`. Parciales en `templates/includes/` |
| CSS CRM | Un solo archivo: `static/css/styles.css` |
| CSS landing | Un solo archivo: `static/css/public.css` |
| Comentarios | Solo el "por qué" — nunca el "qué" |
| Mocks en tests | NEVER — usar base de datos real |
| Abstracciones | NEVER prematuras — tres líneas similares son preferibles |
| Manejo de errores | NEVER para escenarios imposibles en el flujo interno |

---

## 5. Flujo de trabajo obligatorio

1. Verificar índice CodeGraph: `codegraph status` → `codegraph index` si desactualizado.
2. Localizar símbolo/archivo con `codegraph_search` o `codegraph_context` antes de `Read`.
3. Leer solo el fragmento relevante del archivo (nunca el archivo completo si no es necesario).
4. Entregar resumen de máximo 5 líneas: qué entendiste · archivos a revisar · cambios planeados.
5. Esperar aprobación explícita antes de ejecutar cualquier modificación.
6. Aplicar el cambio.
7. Actualizar `PROJECT_CONTEXT.md` si el cambio es estructural o funcional.
8. Actualizar `FRONTEND.md` si el cambio es visual o de UX.

---

## 6. Stop conditions — MANDATORY

Detener y pedir aprobación explícita antes de:
- Eliminar cualquier archivo o modelo.
- Agregar o actualizar dependencias en `requirements.txt`.
- Crear migraciones de base de datos.
- Ejecutar comandos que modifiquen datos en producción.
- Hacer commits, pushes o cualquier operación Git.
- Crear archivos nuevos no solicitados explícitamente.

---

## 7. Riesgos conocidos — no introducir nuevas instancias

| Riesgo | Descripción | Archivo afectado |
|---|---|---|
| Fuga de datos entre tenants | `Lead.objects.all()` sin filtro de workspace | `crm/views.py:126` |
| Lead sin workspace | `demorequest_convert` sin workspace seguro en sesión | `crm/views.py` |
| BOM UTF-16 en requirements | Problemas en CI/CD — ya ocurrió, hay `strip_bom.py` | `requirements.txt` |
| `ia_diagnostico` en INSTALLED_APPS | App skeleton sin vistas ni URLs — no generar migraciones de ella | `ids_web/settings.py` |

NEVER replicar el patrón `Model.objects.all()` sin filtro de workspace en vistas del CRM.

---

## 8. Qué NO hacer — lista definitiva

### Código
- NEVER `Model.objects.all()` sin filtro de workspace en vistas del panel.
- NEVER hardcodear rutas de URL — usar `reverse()` o `{% url %}`.
- NEVER mocks en tests.
- NEVER APIs de Django anteriores a 6.0.
- NEVER abstracciones prematuras.
- NEVER comentarios que expliquen qué hace el código.
- NEVER manejo de errores para escenarios internamente imposibles.

### Archivos y estructura
- NEVER crear archivos nuevos sin solicitud explícita.
- NEVER editar `staticfiles/` — es generado por `collectstatic`.
- NEVER mezclar estilos CSS entre `styles.css` y `public.css`.
- NEVER agregar librerías CSS/JS externas (Bootstrap, Tailwind, jQuery, React) sin aprobación.

### Operaciones Git y sistema
- NEVER hacer commits sin aprobación explícita.
- NEVER hacer push sin aprobación explícita.
- NEVER ejecutar operaciones destructivas sin confirmación.
- NEVER saltar hooks de pre-commit (`--no-verify`).

### Exploración
- NEVER leer `venv/`, `staticfiles/`, `.git/`, `__pycache__/`, `node_modules/`.
- NEVER hacer `Glob` sin excluir esos directorios.
- NEVER re-leer archivos ya inspeccionados en la misma sesión.
- NEVER leer archivos completos cuando CodeGraph puede responder la pregunta estructural.

---

## 9. Funcionalidades implementadas — no reimplementar

- Landing pública con SEO (sitemap, robots.txt, meta tags, blog).
- Formulario de solicitud de demo → `DemoRequest`.
- Nurturing automático por email (días 3, 7, 14) vía management commands.
- CRM multi-tenant: leads, notas, auditoría de cambios (`LeadAuditLog`).
- Conversión `DemoRequest` → `Lead` con aislamiento de workspace.
- Archivado de solicitudes (`status = discarded`).
- RBAC (admin/supervisor/sales/readonly).
- Selector y middleware de workspace activo.
- Agente IA conversacional con base de conocimiento + aprendizaje incremental.
- Auth por email o username (`EmailOrUsernameBackend`).
- Deploy en Render.com (gunicorn + WhiteNoise).
- Email transaccional vía Resend.
- Logout con POST y redirect a solicitudes.
- Header CRM oscuro con fondo limpio.

---

## 10. Funcionalidades pendientes — no implementar sin solicitud

- `ia_diagnostico` — app skeleton en `INSTALLED_APPS`, sin vistas ni URLs.
- Filtros y paginación en lista de leads.
- Tests unitarios e integración (archivos `tests.py` vacíos).
- Gestión de usuarios desde el CRM (invitar, desactivar membresías).
- Integración real con OpenAI API en `agente_ia` (SDK instalado, sin uso en producción).

---

## 11. Dependencias — no agregar sin aprobación

Las dependencias actuales en `requirements.txt` cubren todas las funcionalidades implementadas.
NEVER agregar una nueva dependencia para algo que Django, Python stdlib, o una dependencia existente ya resuelven.
Si una nueva dependencia es necesaria: justificar, proponer, esperar aprobación, luego agregar.

Dependencias clave instaladas (no reinstalar ni duplicar):
`django` · `gunicorn` · `whitenoise` · `dj-database-url` · `psycopg2-binary` · `resend` · `openai` · `requests` · `pydantic`

---

## 12. Resumen de archivos de contexto del proyecto

| Archivo | Propósito |
|---|---|
| `CLAUDE.md` | Reglas de comportamiento de Claude, convenciones de código, flujo de trabajo |
| `PROJECT_CONTEXT.md` | Arquitectura completa, modelos, URLs, dependencias, estado actual, commits |
| `PROJECT_RULES.md` | Este archivo — decisiones permanentes, restricciones transversales, qué no hacer |
| `FRONTEND.md` | Guía visual: identidad, componentes, UX, responsive, criterios de diseño |
