# MediaPanel

Plataforma centralizada para la administración de servidores multimedia (Plex, Emby, Jellyfin), usuarios y revendedores. Este repositorio se encuentra en construcción siguiendo la hoja de ruta descrita en [`docs/roadmap.md`](docs/roadmap.md).

## 📊 Estado del Proyecto

**Fase actual:** Iteración 3 - Configuración de servidores ✅  
**Salud:** 🟢 Sólido - Base funcional con arquitectura moderna  
**Líneas de código:** ~1,370+ líneas (backend) + frontend completo  
**Cobertura:** Autenticación, CRUD multimedia, UI responsive  

### Resumen Técnico
- ✅ **Backend:** NestJS 11 + Prisma + PostgreSQL con JWT auth
- ✅ **Frontend:** Next.js 16 + React 19 + Tailwind CSS 4
- ✅ **Infraestructura:** Docker multi-stage + compose orchestration
- ✅ **Features:** Auth completa, gestión de servidores/usuarios/paquetes multimedia
- 📋 **Próximo:** Rate limiting, BullMQ, integraciones avanzadas

> 💡 **Ver análisis completo y ruta de optimización:** [`docs/04-optimization-roadmap.md`](docs/04-optimization-roadmap.md)

## 🏗️ Estructura actual

```
.
├── docs/                 # Documentación iterativa y roadmap
├── infra/                # Espacio reservado para manifests, IaC, etc.
├── packages/
│   ├── backend/          # API NestJS + Prisma
│   └── frontend/         # Next.js 15 + Tailwind
├── docker-compose.yml    # Orquestación de servicios
└── .env.example          # Variables de entorno base
```

## 🚀 Primer arranque (desarrollo)

> Requisitos: Docker y Docker Compose instalados en el host. Para desarrollo local sin Docker se recomienda Node.js >= 20.x (la aplicación dentro de los contenedores ya usa Node 22).

1. Copia el archivo de variables de entorno y ajusta valores según necesidad:
   ```bash
   cp .env.example .env
   ```
   > Verifica especialmente `POSTGRES_PORT`, `APP_HOST_PORT` y `FRONTEND_HOST_PORT`; por defecto Redis se expone en `6382`, el backend en `5001` y el frontend en `5174` para evitar choques con instalaciones locales. Si accedes desde otra máquina, deja `NEXT_PUBLIC_API_URL=auto` y ajusta `NEXT_PUBLIC_API_PORT` al puerto público del backend.

2. (Opcional) Aplica migraciones y seeds en caso de ejecutar desde el host:
   ```bash
   cd packages/backend
   DATABASE_URL=postgresql://mediapanel:mediapanel@localhost:5442/mediapanel?schema=public \\
     npx prisma migrate dev
   DATABASE_URL=postgresql://mediapanel:mediapanel@localhost:5442/mediapanel?schema=public \\
     npm run prisma:seed
   ```
   > El seed restablece tokens de acceso, crea servidores demo (Plex, Emby, Jellyfin) y carga usuarios multimedia de ejemplo para pruebas.

3. Levanta la infraestructura completa (PostgreSQL, Redis, Mailhog, backend, frontend):
   ```bash
   docker compose up -d --build
   ```

4. Abre tu navegador:
   - Backend health check: http://localhost:5001/api
   - Panel Next.js (dashboard + autenticación): http://localhost:5174
   - Mailhog (correo de desarrollo): http://localhost:8025

5. Para detener los servicios:
   ```bash
   docker compose down
   ```

> Los servicios de base de datos se exponen en el host usando los puertos definidos en `.env` (PostgreSQL 5442, Redis 6382 por defecto). Ajusta estos valores si ya utilizas esos puertos localmente.

## 📚 Documentación

- [`docs/roadmap.md`](docs/roadmap.md): progreso general y próximos hitos.
- [`docs/01-setup.md`](docs/01-setup.md): bitácora detallada de la iteración de setup.
- [`docs/02-auth.md`](docs/02-auth.md): autenticación con JWT, refresh tokens y logout.
- [`docs/03-media-servers.md`](docs/03-media-servers.md): configuración de servidores, integraciones y UI.
- [`docs/04-optimization-roadmap.md`](docs/04-optimization-roadmap.md): **análisis completo y ruta de optimización detallada**.

## 📦 Stack técnico

- **Backend:** NestJS 11 (TypeScript), Prisma ORM, PostgreSQL.
- **Frontend:** Next.js 15 (App Router), Tailwind CSS.
- **Colas / Jobs:** Redis (BullMQ por integrar en próximas iteraciones).
- **Notificaciones:** Mailhog para desarrollo (SMTP), Twilio opcional.
- **Infraestructura:** Docker multi-stage + docker-compose.

## 🧪 Pruebas disponibles

- `cd packages/backend && npm test` · unit tests (health-check, guardas por rol, media servers, integraciones).
- `cd packages/backend && npm run test:e2e` · smoke test del health-check (sin requerir PostgreSQL).
- `cd packages/frontend && npm run lint` · validación estática del frontend (ESLint + TypeScript).
- Crear un usuario multimedia vía API:
  ```bash
  TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"email":"admin@mediapanel.local","password":"Admin123!"}' | jq -r '.accessToken')

  curl -s -X POST http://localhost:5001/api/media-users \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{"displayName":"Demo API","email":"demo@api.local","platform":"PLEX","status":"active","credits":3}' | jq
  ```

## ✅ Estado actual

- Base del monorepo creada y documentada.
- Scaffold de backend y frontend funcionando en Docker.
- Prisma migrado (`init`) con modelos `User`, `Reseller`, `MediaServer`, `MediaUser`.
- Seed automático crea cuentas `admin` y `reseller` con credenciales configurables (ver `.env`).
- Endpoints de autenticación disponibles:
  - `POST /api/auth/login`
  - `POST /api/auth/refresh` (body `{"refreshToken": "<token>"}`)
- `POST /api/auth/logout`
- `GET /api/auth/profile` (requiere `Authorization: Bearer <token>`)
- Endpoint ejemplo protegido por rol ADMIN: `GET /api/users`.
- Gestión de servidores multimedia:
  - `GET /api/config/:service`
  - `POST /api/config/:service`
  - `POST /api/config/:service/test`
  - `POST /api/integrations/jellyfin/export-users`
- Gestión de paquetes multimedia:
  - `GET /api/media-packages`
  - `POST /api/media-packages`
  - `PATCH /api/media-packages/:id`
  - `DELETE /api/media-packages/:id`
  - UI con creación/edición/eliminación optimista, filtros por estado y ordenamiento (Next.js).
- Gestión de usuarios multimedia:
  - `GET /api/media-users` (filtros `service`, `status`, `search`)
  - `POST /api/media-users`
  - `PATCH /api/media-users/:id`
  - `DELETE /api/media-users/:id`
- Frontend renovado con sidebar animado, barra superior fija, modo claro/oscuro persistente y formularios de configuración (Plex, Emby, Jellyfin).
- Capa de estado compartido con Zustand para configuraciones, paquetes y usuarios multimedia.
- Vista `/[servicio]/users` consume la API de usuarios multimedia y muestra métricas dinámicas (exportación disponible en Jellyfin).
- Vista `/[servicio]/packages` permite administrar paquetes con modales, filtros activos/inactivos, ordenamiento y sincronización manual.

### Credenciales semilla por defecto

| Rol       | Usuario                         | Contraseña   |
|-----------|---------------------------------|--------------|
| Admin     | `admin@mediapanel.local`        | `Admin123!`  |
| Reseller  | `reseller@mediapanel.local`     | `Reseller123!` |

Puedes modificar estos valores en `.env` (`SEED_*`) antes de ejecutar `npm run prisma:seed`.

## 🧭 Próximos pasos (resumen)

1. Rotar e invalidar refresh tokens de forma granular y auditar sesiones.
2. Construir módulos pendientes para revendedores y automatizaciones avanzadas.
3. Integrar BullMQ + Redis para jobs automáticos.
4. Desarrollar interfaz completa en Next.js (dashboard, formularios, estado remoto).
5. Extender RBAC para roles `support` y `viewer` en endpoints reales.

Para más detalles y seguimiento, revisa el roadmap.
