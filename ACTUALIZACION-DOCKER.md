# 🔄 GUÍA DE ACTUALIZACIÓN - DOCKER

## ✅ HAS ACTUALIZADO EL PROYECTO EXISTENTE

Los siguientes módulos y componentes han sido **agregados** a tu proyecto Docker:

### 🆕 NUEVOS MÓDULOS BACKEND
- ✅ `calendar/` - Calendario y vencimientos
- ✅ `dashboard/` - Métricas y alertas
- ✅ Mejoras en `media-users/` - Sistema de créditos

### 🆕 NUEVOS COMPONENTES FRONTEND
- ✅ `dashboard-new/` - 6 componentes modernos
- ✅ `/dashboard` - Página completa nueva

---

## 🚀 CÓMO APLICAR LOS CAMBIOS

### Opción 1: Script Automático (Recomendado)

```bash
cd /root/Panelplex
./actualizar-docker.sh
```

Este script:
1. ✅ Detiene los contenedores
2. ✅ Reconstruye backend (con Calendar y Dashboard)
3. ✅ Reconstruye frontend (con componentes nuevos)
4. ✅ Inicia todos los servicios
5. ✅ Muestra logs en tiempo real

---

### Opción 2: Comandos Manuales

```bash
cd /root/Panelplex

# Detener contenedores
docker compose down

# Reconstruir backend con nuevos módulos
docker compose build backend --no-cache

# Reconstruir frontend con nuevos componentes
docker compose build frontend --no-cache

# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f
```

---

## 🎯 VERIFICAR QUE TODO FUNCIONA

### 1. Verificar servicios
```bash
docker compose ps
```

Deberías ver:
- ✅ mediapanel_db (healthy)
- ✅ mediapanel_backend (running)
- ✅ mediapanel_frontend (running)
- ✅ mediapanel_redis (running)
- ✅ mediapanel_mailhog (running)

### 2. Acceder al dashboard nuevo
```
http://localhost:5174/dashboard
```

### 3. Probar endpoints nuevos

**Obtén un token primero:**
```bash
# Login
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"tupassword"}'
```

**Prueba los endpoints nuevos:**
```bash
TOKEN="tu_access_token_aqui"

# Dashboard metrics
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/dashboard/metrics

# Calendar events
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/calendar/events

# Alertas
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/dashboard/alerts
```

### 4. Usar el script de testing
```bash
TOKEN=tu_token ./test-endpoints.sh
```

---

## 📊 NUEVAS RUTAS DISPONIBLES

| Ruta | Descripción | Estado |
|------|-------------|--------|
| `/dashboard` | Dashboard completo con métricas | ✅ NUEVO |
| `/calendar` (API) | Endpoints de calendario | ✅ NUEVO |
| `/dashboard/*` (API) | Endpoints de métricas | ✅ NUEVO |

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Backend no compila
```bash
# Verificar que app.module.ts tiene los imports
cd /root/Panelplex/packages/backend
cat src/app.module.ts | grep -E "(Calendar|Dashboard)"

# Debería mostrar:
# import { CalendarModule } from './calendar/calendar.module';
# import { DashboardModule } from './dashboard/dashboard.module';
```

### Frontend no muestra dashboard
```bash
# Verificar que existe la página
ls -la /root/Panelplex/packages/frontend/src/app/\(panel\)/dashboard/

# Debería mostrar: page.tsx
```

### Contenedores no inician
```bash
# Ver logs de error
docker compose logs backend
docker compose logs frontend

# Reintentar build
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Puerto en uso
Si ves errores de puerto, verifica:
```bash
# Ver qué está usando el puerto
sudo netstat -tlnp | grep -E "(5174|3001|5442)"

# O detén todo y reinicia
docker compose down
docker compose up -d
```

---

## 📝 CAMBIOS EN LA BASE DE DATOS

**No necesitas ejecutar migraciones nuevas**, los módulos nuevos usan las tablas existentes:
- `MediaUser` - Ya existe
- `MediaServer` - Ya existe
- No se agregaron nuevas tablas

---

## ✨ NUEVAS FUNCIONALIDADES DISPONIBLES

Después de actualizar Docker, tendrás:

### 📊 Dashboard
- Métricas en tiempo real
- 6 tarjetas informativas
- Auto-refresh cada 60s
- Estadísticas por servidor

### 📅 Calendario
- Vista mensual completa
- Colores por estado (verde/amarillo/rojo)
- Click para ver detalles
- Navegación fluida

### 🚨 Alertas
- Priorizadas automáticamente
- Vencimientos hoy/mañana
- Servidores caídos
- Auto-refresh cada 2 minutos

### 👤 Usuarios
- Botones interactivos en cada tarjeta
- Recargar créditos con modal
- Suspender/Activar
- Ver detalles completos

---

## 📚 DOCUMENTACIÓN

- **INICIO-RAPIDO.md** - Guía completa
- **FUNCIONALIDADES-COMPLETAS.md** - Documentación técnica
- **RESUMEN-VISUAL.txt** - Resumen visual
- **test-endpoints.sh** - Script de pruebas

---

## 🎉 ¡LISTO!

Ejecuta el script y tendrás todas las funcionalidades nuevas:

```bash
./actualizar-docker.sh
```

Luego accede a:
```
http://localhost:5174/dashboard
```

**¡Disfruta de tu panel mejorado!** 🚀
