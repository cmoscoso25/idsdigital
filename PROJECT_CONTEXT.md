# PROJECT_CONTEXT.md — IDS Digital

**Última actualización:** 2026-06-04

---

## Resumen ejecutivo

**IDS Digital** es una plataforma web SaaS de la empresa Inteligencia Digital SpA (idsdigital.cl).
Combina un sitio público de marketing con un CRM interno multi-tenant y un agente de IA conversacional.
Stack: Django 6.0.2 · Python 3.11 · PostgreSQL (producción) · SQLite (desarrollo) · Deploy en Render.com.

---

## Arquitectura detectada

```
Intelegencia_Digital/
├── ids_web/            # Proyecto Django (settings, urls raíz, wsgi/asgi)
├── core/               # Health check y vistas genéricas
├── accounts/           # Auth custom: User, Workspace, Membership, RBAC
├── public/             # Landing, blog, formulario demo, nurturing email
├── crm/                # CRM interno: Lead, DemoRequest, LeadNote, LeadAuditLog
├── agente_ia/          # Agente conversacional con base de conocimiento propia
├── ia_diagnostico/     # App pendiente/skeleton (sin vistas ni URLs activas)
├── templates/          # Templates globales + por app
├── static/             # CSS, JS, imágenes (fuente)
├── staticfiles/        # Generado por collectstatic (no editar)
└── ids_web_final/      # Carpeta legacy/standalone (landing HTML estático)
```

**Multi-tenancy:** Middleware `CurrentWorkspaceMiddleware` inyecta `request.workspace` en cada
request autenticado desde la sesión (`current_workspace_id`).

**RBAC:** Roles `admin / supervisor / sales / readonly` definidos en `accounts.Membership`.

---

## Aplicaciones principales

| App | Propósito | Estado |
|---|---|---|
| `public` | Landing, blog SEO, formulario demo, nurturing, Nexa AI landing | Activo |
| `crm` | Gestión de leads y solicitudes de demo | Activo |
| `accounts` | Auth, workspaces, RBAC | Activo |
| `agente_ia` | Chatbot con base de conocimiento propia | Activo |
| `core` | Health check, vista home redirect | Activo |
| `nexa` | SaaS privado Nexa AI: empresas, memoria de marca, generación de contenido IA | MVP activo |
| `ia_diagnostico` | Diagnóstico IA (skeleton, sin URLs) | Pendiente |

---

## URLs críticas

| Ruta | View | Descripción |
|---|---|---|
| `/` | `public.landing` | Landing pública |
| `/health/` | `core.health_check` | Healthcheck Render |
| `/accounts/login/` | `accounts.AccountsLoginView` | Login CRM |
| `/accounts/logout/` | `accounts.AccountsLogoutView` | Logout (POST) |
| `/accounts/workspace/` | `accounts.workspace_select` | Selector de workspace |
| `/panel/solicitudes/` | `crm.demorequest_list` | Solicitudes de demo (CRM) |
| `/panel/solicitudes/<id>/` | `crm.demorequest_detail` | Detalle solicitud |
| `/panel/solicitudes/<id>/convertir/` | `crm.demorequest_convert` | Conversión a lead |
| `/panel/solicitudes/<id>/archivar/` | `crm.demorequest_archive` | Archivar solicitud |
| `/panel/leads/` | `crm.lead_list` | Leads CRM |
| `/panel/leads/<id>/` | `crm.lead_detail` | Detalle lead |
| `/panel/leads/<id>/estado/` | `crm.lead_change_status` | Cambio de estado (POST) |
| `/agente-ia/` | `agente_ia` (namespace) | Chatbot IA |
| `/blog/` | `public.blog_list` | Blog público |
| `/blog/<slug>/` | `public.blog_detail` | Artículo de blog |
| `/servicios/` | `public.services` | Página de servicios |
| `/automatizacion-procesos/` | `public.automation_processes` | Página SEO |
| `/desarrollo-software-medida/` | `public.custom_software_development` | Página SEO |
| `/inteligencia-artificial-empresas/` | `public.ai_solutions` | Página SEO |
| `/nexa/` | `public.nexa` | Landing pública Nexa AI by IDS Digital |
| `/nexa/app/` | `nexa.dashboard` | Dashboard privado Nexa AI (login_required) |
| `/nexa/app/empresas/` | `nexa.empresa_list` | Lista de empresas del usuario |
| `/nexa/app/empresas/nueva/` | `nexa.empresa_nueva` | Crear empresa |
| `/nexa/app/empresas/<id>/` | `nexa.empresa_detalle` | Detalle empresa + memoria |
| `/nexa/app/empresas/<id>/memoria/` | `nexa.memoria_editar` | Crear / editar memoria de marca |
| `/nexa/app/empresas/<id>/generar/` | `nexa.generar` | Generar contenido con IA |
| `/nexa/app/contenidos/` | `nexa.contenido_list` | Biblioteca de contenidos |
| `/nexa/app/contenidos/<id>/` | `nexa.contenido_detalle` | Detalle + cambio de estado |
| `/admin/` | Django Admin | Administración interna |
| `/sitemap.xml` | Django Sitemaps | SEO |
| `/robots.txt` | `public.robots_txt` | SEO |

---

## Modelos principales

### `accounts`
- **User** — AbstractUser corporativo (sin tenant directo, soporta multi-workspace)
- **Workspace** — Tenant (empresa/unidad): name, legal_name, rut, email, phone
- **Membership** — Relación User↔Workspace con rol RBAC; unique_together (user, workspace)

### `public`
- **DemoRequest** — Solicitudes del formulario público; nurturing por email (días 3, 7, 14); conversión a Lead
- **BlogPost** — Blog con SEO (slug, meta_title, meta_description, meta_keywords, categoría)

### `crm`
- **Lead** — Lead de ventas aislado por workspace; estados: nuevo → en_gestion → cotizado → cerrado/perdido; constraint unique (workspace, email)
- **LeadNote** — Notas internas asociadas al lead
- **LeadAuditLog** — Auditoría de cambios (stage, owner, notas) con before/after JSON

### `nexa`
- **EmpresaNexa** — Empresa registrada por un usuario en Nexa AI: nombre, rubro, descripción, público objetivo, tono de marca, objetivo principal, instagram, sitio_web, logo (ImageField), colores hex, fecha_creacion. FK a `accounts.User`.
- **MemoriaMarca** — OneToOne con EmpresaNexa: propuesta_valor, servicios_principales, palabras_clave, estilo_comunicacion, evitar_mencionar, instrucciones_ia, resumen_marca. Contexto para agentes IA.
- **ContenidoGenerado** — Contenido generado por IA para una empresa: tipo (carrusel/historia/post/reel/campaña), titulo, copy, hashtags, cta, estructura_json, estado (borrador/aprobado/programado/publicado), fecha_programada, fecha_creacion.

### `agente_ia`
- **CategoriaConocimiento** — Categorías de la base de conocimiento del chatbot
- **RespuestaConocimiento** — Respuestas con palabras clave, prioridad y contador de uso
- **PreguntaAprendida** — Preguntas sin respuesta para aprendizaje incremental
- **ConversacionAgente** / **MensajeAgente** — Historial de conversaciones del chatbot

---

## Archivos CSS / JS

| Archivo | Uso |
|---|---|
| `static/css/styles.css` | CRM interno (panel) |
| `static/css/public.css` | Landing (`.landing-page`), Blog (`.blog-dark`) y páginas públicas |
| `static/css/nexa.css` | Landing Nexa AI (`.nexa-page`) — cargado solo en `/nexa/` |
| `static/css/nexa_app.css` | Panel privado Nexa AI (`.nxa-app`) — cargado solo en `/nexa/app/*` |
| `static/js/diagnostico_ia.js` | Frontend del agente conversacional |
| `static/css/diagnostico_ia.css` | Estilos del chatbot |

---

## Dependencias importantes

| Paquete | Versión | Uso |
|---|---|---|
| Django | 6.0.2 | Framework principal |
| gunicorn | 25.3.0 | WSGI server (producción) |
| whitenoise | 6.12.0 | Archivos estáticos sin S3 |
| dj-database-url | 3.1.2 | Config DB por variable de entorno |
| psycopg2-binary | 2.9.12 | PostgreSQL (producción) |
| resend | 2.30.1 | Email transaccional |
| openai | 2.34.0 | SDK OpenAI (instalado, uso no confirmado en producción) |
| requests | 2.34.2 | HTTP client |
| pydantic | 2.13.4 | Validación de datos |

---

## Funcionalidades implementadas

- [x] Landing pública con SEO (sitemap, robots.txt, meta tags)
- [x] Blog con slugs y meta SEO
- [x] Formulario de solicitud de demo → DemoRequest
- [x] Nurturing automático por email (días 3, 7, 14) vía management commands
- [x] CRM multi-tenant: leads, notas, auditoría de cambios
- [x] Conversión DemoRequest → Lead (con aislamiento de workspace)
- [x] Archivado de solicitudes (via `status = discarded`)
- [x] RBAC (admin/supervisor/sales/readonly)
- [x] Selector y middleware de workspace activo
- [x] Agente IA conversacional con base de conocimiento + aprendizaje incremental
- [x] Auth por email o username (`EmailOrUsernameBackend`)
- [x] Deploy en Render.com (gunicorn + WhiteNoise)
- [x] Email transaccional vía Resend
- [x] Nexa AI MVP: app `nexa` con modelos, vistas, templates, servicio IA simulado y admin

---

## Sub-SaaS en desarrollo

### Nexa AI by IDS Digital (`/nexa/` + `/nexa/app/`)
Plataforma de marketing digital con agentes de IA para pymes y empresas.
- **Estado:** MVP real implementado como app Django `nexa`. Landing pública en `/nexa/`. Panel privado en `/nexa/app/`.
- **App:** `nexa/` — modelos: `EmpresaNexa`, `MemoriaMarca`, `ContenidoGenerado`.
- **Servicio IA:** `nexa/services/generador_contenido.py` — actualmente simulado, preparado para conectar con Claude/OpenAI API (punto de conexión marcado en el código).
- **Template base:** `templates/nexa/base_nexa.html` — sidebar layout, diseño dark SaaS premium.
- **CSS:** `static/css/nexa_app.css` — scoped bajo `.nxa-app`.
- **Formulario landing:** reutiliza `DemoRequest` con `necesidad = "Nexa AI — Demo anticipada"`.
- **Próximos pasos:**
  - [ ] Conectar `generador_contenido.py` con Claude API (Anthropic SDK ya en requirements)
  - [ ] Integración Meta Graph API para publicación en Instagram/Facebook
  - [ ] Sistema de agentes IA especializados (Estratega, Copywriter, Community Manager)
  - [ ] Planes y pagos (Stripe)
  - [ ] Botón "Entrar a Nexa" en landing `/nexa/` → `/nexa/app/`
  - [ ] Paginación en biblioteca de contenidos

## Funcionalidades pendientes

- [ ] `ia_diagnostico` — app en INSTALLED_APPS sin vistas ni URLs
- [ ] Filtros y paginación en lista de leads (actualmente sin paginar)
- [ ] Tests unitarios e integración (archivos `tests.py` vacíos)
- [ ] Gestión de usuarios desde el CRM (invitar, desactivar membresías)
- [ ] Integración real con OpenAI API en agente_ia (el paquete está instalado pero el servicio usa solo base de conocimiento local)

---

## Riesgos conocidos

1. **Fuga de datos entre tenants:** `crm/views.py:126` — `Lead.objects.all()` sin filtrar por workspace. Cualquier usuario autenticado ve todos los leads de todos los workspaces.
2. **`demorequest_convert` sin workspace seguro:** si `request.user` no tiene workspace en sesión, el lead se crea sin workspace y viola el constraint NOT NULL.
3. **`requirements.txt` con encoding BOM UTF-16:** puede causar problemas en CI/CD (hay un script `strip_bom.py` que indica que ya ocurrió este problema).
4. **`ia_diagnostico` en INSTALLED_APPS sin migraciones funcionales:** puede generar confusión en el estado del proyecto.

---

## Últimas decisiones técnicas (por commits)

| Commit | Decisión |
|---|---|
| Pendiente | Rediseño landing v2: Inter font, canvas partículas, aurora CSS, reveal on scroll |
| `8d33e5d` | Rediseño landing dark premium + sistema de documentación (FRONTEND/DESIGN_SYSTEM/PROJECT_RULES) |
| `d168965` | Limpieza y optimización de styles.css |
| `fe230c6` | Header CRM oscuro con fondo limpio |
| `b3bc6b1` | Logout con POST y redirects a solicitudes |
| `b534f2e` | Logout redirige correctamente al login del CRM |
| `c872569` | Rediseño CRM alineado con la landing |

- Auth con `EmailOrUsernameBackend` para flexibilidad de login.
- WhiteNoise en lugar de S3/CDN para simplicidad en Render.
- Agente IA con base de conocimiento propia (sin OpenAI en producción actualmente).
