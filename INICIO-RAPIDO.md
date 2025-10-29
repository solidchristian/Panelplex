# 🚀 Inicio Rápido - Panel Multimedia

## 📋 Requisitos Previos

- Node.js 20+
- PostgreSQL (o usar Docker)
- npm o yarn

## 🏁 Inicio Rápido (con Docker)

### 1. Iniciar servicios con Docker Compose

```bash
cd /root/Panelplex
docker compose up -d
```

Esto iniciará:
- PostgreSQL (puerto 5432)
- Backend NestJS (puerto 3001)
- Frontend Next.js (puerto 3000)

### 2. Acceder a la aplicación

```
Frontend: http://localhost:3000
Backend API: http://localhost:3001
```

---

## 🛠️ Inicio Manual (sin Docker)

### Backend

```bash
cd /root/Panelplex/packages/backend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Generar cliente Prisma
npx prisma generate

# Ejecutar migraciones
npx prisma migrate deploy

# Iniciar en modo desarrollo
npm run start:dev
```

### Frontend

```bash
cd /root/Panelplex/packages/frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
echo "NEXT_PUBLIC_API_URL=http://localhost:3001" > .env.local

# Iniciar en modo desarrollo
npm run dev
```

---

## 🎯 Funcionalidades Principales

### 📊 Dashboard
Accede al dashboard completo en: **http://localhost:3000/dashboard**

**Características:**
- ✅ Métricas en tiempo real
- ✅ Alertas y notificaciones
- ✅ Calendario de vencimientos
- ✅ Actividad reciente
- ✅ Estado de servidores

### 👥 Gestión de Usuarios

**Crear usuario:**
```bash
POST /media-users
{
  "displayName": "Juan Pérez",
  "email": "juan@example.com",
  "platform": "JELLYFIN",
  "credits": 3,
  "status": "active"
}
```

**Agregar créditos:**
```bash
POST /media-users/:id/add-credits
{
  "credits": 2
}
```

**Suspender usuario:**
```bash
POST /media-users/:id/suspend
```

### 📅 Calendario

**Ver eventos del mes:**
```bash
GET /calendar/events?year=2025&month=1
```

**Vencimientos próximos:**
```bash
GET /calendar/upcoming?days=7
```

### 📈 Dashboard Métricas

**Obtener métricas:**
```bash
GET /dashboard/metrics
```

**Obtener alertas:**
```bash
GET /dashboard/alerts
```

---

## 🧪 Probar Endpoints

### Usando el script de pruebas

```bash
cd /root/Panelplex

# Primero obtén un token de autenticación
# Luego ejecuta:
TOKEN=tu_jwt_token ./test-endpoints.sh
```

### Usando curl manualmente

```bash
# Obtener token (login)
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"tupassword"}'

# Usar el token en requests
TOKEN="tu_access_token_aqui"

# Métricas del dashboard
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/dashboard/metrics

# Calendario
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/calendar/events?year=2025&month=1

# Usuarios
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/media-users
```

---

## 🎨 Rutas del Frontend

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal |
| `/dashboard` | Dashboard completo con métricas, alertas y calendario |
| `/servers` | Configuración de servidores |
| `/plex/users` | Usuarios de Plex |
| `/emby/users` | Usuarios de Emby |
| `/jellyfin/users` | Usuarios de Jellyfin |
| `/config/plex` | Configurar servidor Plex |
| `/config/emby` | Configurar servidor Emby |
| `/config/jellyfin` | Configurar servidor Jellyfin |

---

## 📚 Endpoints API Principales

### Dashboard
- `GET /dashboard/metrics` - Métricas principales
- `GET /dashboard/alerts` - Alertas y notificaciones
- `GET /dashboard/summary` - Resumen completo
- `GET /dashboard/recent-activity` - Actividad reciente
- `GET /dashboard/expiration-chart` - Gráfico de vencimientos
- `GET /dashboard/servers-status` - Estado de servidores

### Calendar
- `GET /calendar/events` - Eventos del mes
- `GET /calendar/upcoming` - Vencimientos próximos
- `GET /calendar/expired` - Usuarios vencidos
- `GET /calendar/stats` - Estadísticas

### Media Users
- `GET /media-users` - Listar usuarios
- `GET /media-users/stats` - Estadísticas
- `GET /media-users/:id` - Obtener usuario
- `POST /media-users` - Crear usuario
- `PATCH /media-users/:id` - Actualizar usuario
- `DELETE /media-users/:id` - Eliminar usuario
- `POST /media-users/:id/add-credits` - Agregar créditos
- `POST /media-users/:id/suspend` - Suspender
- `POST /media-users/:id/activate` - Activar
- `POST /media-users/bulk-delete` - Eliminar múltiples

### Media Servers
- `GET /media-servers` - Listar servidores
- `PUT /media-servers/:type` - Configurar servidor
- `DELETE /media-servers/:type` - Eliminar servidor
- `POST /media-servers/:type/test` - Probar conexión

### Integrations
- `POST /integrations/jellyfin/export-users` - Exportar usuarios Jellyfin
- `POST /integrations/jellyfin/import-users` - Importar usuarios Jellyfin
- `POST /integrations/emby/export-users` - Exportar usuarios Emby
- `POST /integrations/emby/import-users` - Importar usuarios Emby
- `POST /integrations/plex/export-users` - Exportar usuarios Plex
- `POST /integrations/plex/import-users` - Importar usuarios Plex

---

## 🔧 Configuración de Servidores

### Configurar Jellyfin

```bash
PUT /media-servers/JELLYFIN
{
  "name": "Mi Servidor Jellyfin",
  "baseUrl": "http://jellyfin.example.com",
  "port": 8096,
  "apiKey": "tu_api_key_aqui",
  "active": true
}
```

### Configurar Emby

```bash
PUT /media-servers/EMBY
{
  "name": "Mi Servidor Emby",
  "baseUrl": "http://emby.example.com",
  "port": 8096,
  "apiKey": "tu_api_key_aqui",
  "active": true
}
```

### Configurar Plex

```bash
PUT /media-servers/PLEX
{
  "name": "Mi Servidor Plex",
  "baseUrl": "http://plex.example.com",
  "port": 32400,
  "apiKey": "tu_plex_token_aqui",
  "active": true
}
```

---

## 🎯 Sistema de Créditos

- **1 crédito = 1 mes de servicio**
- Al agregar créditos, la fecha de vencimiento se extiende automáticamente
- Si el usuario ya está vencido, comienza desde la fecha actual
- Los créditos se descuentan automáticamente cada mes (requiere job scheduler)

**Ejemplo:**
```javascript
// Usuario vence el 2025-01-15
// Hoy es 2025-01-10
// Agregamos 2 créditos
// Nueva fecha de vencimiento: 2025-03-15

// Usuario vence el 2025-01-05 (ya vencido)
// Hoy es 2025-01-10
// Agregamos 1 crédito
// Nueva fecha de vencimiento: 2025-02-10
```

---

## 🎨 Estados y Colores

### Estados de Usuario
- 🟢 **ACTIVO** - Más de 7 días restantes
- 🟡 **POR VENCER** - 7 días o menos restantes
- 🔴 **VENCIDO** - Fecha de vencimiento pasada
- ⚫ **SUSPENDIDO** - Usuario pausado manualmente

### Prioridades de Alertas
- 🔴 **CRÍTICO** - Servidores caídos
- 🔴 **ALTO** - Usuarios vencidos, vencen hoy
- 🟡 **MEDIO** - Vencen mañana
- 🔵 **BAJO** - Informativo

---

## 📖 Documentación Completa

Para más detalles, consulta:
- [`FUNCIONALIDADES-COMPLETAS.md`](./FUNCIONALIDADES-COMPLETAS.md) - Documentación técnica completa
- [`README.md`](./README.md) - Información general del proyecto
- [`docs/`](./docs/) - Documentación adicional

---

## 🐛 Solución de Problemas

### Backend no inicia

```bash
# Verificar PostgreSQL
psql -h localhost -U postgres -c "SELECT version();"

# Regenerar Prisma
cd packages/backend
npx prisma generate
npx prisma migrate deploy

# Limpiar y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Frontend no carga

```bash
# Verificar variable de entorno
cat packages/frontend/.env.local
# Debe contener: NEXT_PUBLIC_API_URL=http://localhost:3001

# Limpiar caché de Next.js
cd packages/frontend
rm -rf .next
npm run dev
```

### Error de autenticación

```bash
# Verificar que el token no haya expirado
# Los tokens expiran cada 15 minutos por defecto
# Usa el refresh token para obtener uno nuevo

curl -X POST http://localhost:3001/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refreshToken":"tu_refresh_token"}'
```

---

## 🚀 Despliegue en Producción

### Variables de entorno requeridas

**Backend (.env):**
```env
DATABASE_URL="postgresql://user:password@host:5432/dbname"
JWT_SECRET="tu_secreto_muy_seguro_aqui"
JWT_EXPIRES_IN="15m"
REFRESH_TOKEN_EXPIRES_IN="7d"
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com
```

### Build para producción

```bash
# Backend
cd packages/backend
npm run build
npm run start:prod

# Frontend
cd packages/frontend
npm run build
npm run start
```

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisa la documentación completa en `FUNCIONALIDADES-COMPLETAS.md`
2. Verifica los logs del backend: `docker compose logs backend`
3. Verifica los logs del frontend: `docker compose logs frontend`

---

**🎉 ¡Listo para usar!**

Accede a http://localhost:3000/dashboard y comienza a gestionar tus usuarios multimedia.
