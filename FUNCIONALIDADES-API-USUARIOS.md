# 🚀 Funcionalidades de API para Usuarios Multimedia

## 📋 Resumen
Se han implementado endpoints completos para **sincronizar usuarios** entre el panel de administración y los servidores multimedia (Jellyfin, Plex, Emby).

---

## 🔧 Endpoints Implementados

### **JELLYFIN**

#### 1. Exportar Usuarios de Jellyfin
**Endpoint:** `POST /integrations/jellyfin/export-users`  
**Descripción:** Obtiene la lista de usuarios del servidor Jellyfin configurado.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Exportación completada correctamente.",
  "usuarios": [
    {
      "id": "abc123",
      "nombre": "Usuario1",
      "ultimoAcceso": "2025-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. Importar Usuarios desde Jellyfin
**Endpoint:** `POST /integrations/jellyfin/import-users`  
**Descripción:** Sincroniza usuarios del servidor Jellyfin al panel. Solo importa usuarios nuevos.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Importación completada: 5 usuarios nuevos, 3 ya existían.",
  "importados": 5,
  "omitidos": 3
}
```

#### 3. Crear Usuario en Jellyfin
**Endpoint:** `POST /integrations/jellyfin/create-user`  
**Body:**
```json
{
  "displayName": "NuevoUsuario",
  "password": "Password123!"
}
```
**Descripción:** Crea un usuario en Jellyfin y lo sincroniza automáticamente al panel.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Usuario creado en Jellyfin y sincronizado con el panel.",
  "usuario": {
    "id": "xyz789",
    "nombre": "NuevoUsuario"
  }
}
```

---

### **PLEX**

#### 1. Exportar Usuarios de Plex
**Endpoint:** `POST /integrations/plex/export-users`  
**Descripción:** Obtiene la lista de usuarios del servidor Plex configurado.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Exportación completada correctamente.",
  "usuarios": [
    {
      "id": "12345",
      "nombre": "UsuarioPlex",
      "email": "usuario@example.com"
    }
  ]
}
```

#### 2. Importar Usuarios desde Plex
**Endpoint:** `POST /integrations/plex/import-users`  
**Descripción:** Sincroniza usuarios del servidor Plex al panel.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Importación completada: 8 usuarios nuevos, 2 ya existían.",
  "importados": 8,
  "omitidos": 2
}
```

---

### **EMBY**

#### 1. Exportar Usuarios de Emby
**Endpoint:** `POST /integrations/emby/export-users`  
**Descripción:** Obtiene la lista de usuarios del servidor Emby configurado.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Exportación completada correctamente.",
  "usuarios": [
    {
      "id": "emby123",
      "nombre": "UsuarioEmby",
      "ultimoAcceso": "2025-01-15T12:00:00Z"
    }
  ]
}
```

#### 2. Importar Usuarios desde Emby
**Endpoint:** `POST /integrations/emby/import-users`  
**Descripción:** Sincroniza usuarios del servidor Emby al panel.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Importación completada: 4 usuarios nuevos, 1 ya existía.",
  "importados": 4,
  "omitidos": 1
}
```

#### 3. Crear Usuario en Emby
**Endpoint:** `POST /integrations/emby/create-user`  
**Body:**
```json
{
  "displayName": "NuevoUsuarioEmby",
  "password": "Password123!"
}
```
**Descripción:** Crea un usuario en Emby y lo sincroniza automáticamente al panel.  
**Respuesta:**
```json
{
  "estado": "ok",
  "mensaje": "Usuario creado en Emby y sincronizado con el panel.",
  "usuario": {
    "id": "emby456",
    "nombre": "NuevoUsuarioEmby"
  }
}
```

---

## 🔐 Autenticación
Todos los endpoints requieren autenticación JWT y roles específicos:
- **Exportar usuarios:** ADMIN, RESELLER, SUPPORT
- **Importar usuarios:** ADMIN, RESELLER
- **Crear usuarios:** ADMIN, RESELLER

---

## 📡 Configuración de Servidores

Antes de usar estos endpoints, asegúrate de tener configurados los servidores en:
- **Jellyfin:** `POST /media-servers/JELLYFIN`
- **Plex:** `POST /media-servers/PLEX`
- **Emby:** `POST /media-servers/EMBY`

**Datos requeridos:**
```json
{
  "name": "Mi Servidor Jellyfin",
  "baseUrl": "http://192.168.1.100",
  "port": 8096,
  "apiKey": "tu-api-key-aqui",
  "active": true
}
```

---

## 🎯 Flujo de Trabajo Recomendado

### **Opción 1: Sincronizar usuarios existentes**
1. Configurar servidor (Jellyfin/Plex/Emby)
2. Llamar a `export-users` para ver usuarios disponibles
3. Llamar a `import-users` para sincronizarlos al panel

### **Opción 2: Crear usuarios desde el panel**
1. Configurar servidor (Jellyfin/Emby)
2. Llamar a `create-user` con nombre y contraseña
3. El usuario se crea en el servidor y en el panel automáticamente

---

## ⚠️ Notas Importantes

### **Jellyfin y Emby**
- Usan la misma API base (Emby fork)
- Requieren header `X-Emby-Token` con el API Key
- Soportan creación de usuarios directamente

### **Plex**
- Requiere header `X-Plex-Token` con el API Key
- La creación de usuarios es más compleja (requiere invitaciones)
- Por ahora solo soporta exportación/importación

### **Prevención de Duplicados**
- Al importar, se verifica el `externalId` para evitar duplicados
- Los usuarios ya existentes se omiten automáticamente

---

## 🧪 Pruebas con cURL

```bash
# Exportar usuarios de Jellyfin
curl -X POST http://192.168.3.180:5001/integrations/jellyfin/export-users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Importar usuarios de Jellyfin
curl -X POST http://192.168.3.180:5001/integrations/jellyfin/import-users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Crear usuario en Jellyfin
curl -X POST http://192.168.3.180:5001/integrations/jellyfin/create-user \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "TestUser",
    "password": "TestPassword123!"
  }'
```

---

## 📊 Estructura de Base de Datos

Los usuarios importados se guardan en la tabla `MediaUser` con:
- `displayName`: Nombre del usuario
- `externalId`: ID del usuario en el servidor externo
- `platform`: JELLYFIN | PLEX | EMBY
- `status`: active | inactive | suspended
- `credits`: Créditos disponibles (default 0)
- `email`: Email del usuario (si está disponible)
- `expiresAt`: Fecha de expiración (opcional)

---

## 🔄 Próximas Mejoras Sugeridas

1. **Sincronización bidireccional:** Actualizar usuarios en el servidor desde el panel
2. **Eliminación de usuarios:** Endpoint para eliminar usuarios del servidor
3. **Actualización de permisos:** Modificar roles y permisos desde el panel
4. **Sincronización automática:** Cron job para sincronizar usuarios periódicamente
5. **Webhooks:** Notificaciones cuando se crean/modifican usuarios
6. **Plex Share:** Implementar invitaciones para Plex

---

## 📝 Cambios Realizados

### Archivos Modificados:
1. **`packages/backend/src/integrations/integrations.service.ts`**
   - Implementadas funciones completas para Jellyfin, Plex y Emby
   - Manejo de errores mejorado
   - Tipado TypeScript para respuestas de APIs

2. **`packages/backend/src/integrations/integrations.controller.ts`**
   - Agregados endpoints para exportar, importar y crear usuarios
   - Configurados guards de autenticación y roles

3. **`packages/backend/src/integrations/integrations.module.ts`**
   - Importado PrismaModule para acceso a base de datos

---

## ✅ Estado Actual
- ✅ Backend desplegado y funcionando
- ✅ Endpoints disponibles en `http://192.168.3.180:5001`
- ✅ Frontend disponible en `http://192.168.3.180:5174`
- ✅ Integración con Jellyfin, Plex y Emby lista

🎉 **¡El sistema está listo para sincronizar usuarios!**
