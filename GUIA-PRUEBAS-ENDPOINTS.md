# 🧪 Guía de Pruebas - Endpoints de Sincronización de Usuarios

## 🎯 Objetivo
Esta guía te muestra cómo probar los nuevos endpoints de sincronización de usuarios paso a paso.

---

## 📋 Prerequisitos

1. ✅ Backend corriendo en `http://192.168.3.180:5001`
2. ✅ Frontend corriendo en `http://192.168.3.180:5174`
3. ✅ Cuenta de admin creada
4. ✅ Servidor multimedia configurado (Jellyfin/Plex/Emby)

---

## 🔐 Paso 1: Obtener Token de Autenticación

### **Opción A: Desde el navegador (DevTools)**
1. Abre `http://192.168.3.180:5174`
2. Inicia sesión con:
   - Email: `admin@mediapanel.local`
   - Password: `Admin123!.`
3. Abre DevTools (F12)
4. Ve a: **Application > Local Storage > http://192.168.3.180:5174**
5. Busca la clave `token` o `authToken`
6. Copia el valor (JWT token)

### **Opción B: Con cURL**
```bash
curl -X POST http://192.168.3.180:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mediapanel.local",
    "password": "Admin123!."
  }'
```

**Respuesta esperada:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "...",
  "user": {
    "id": "...",
    "email": "admin@mediapanel.local",
    "role": "ADMIN"
  }
}
```

**Guarda el `accessToken`** - lo necesitarás para los siguientes pasos.

---

## 🔧 Paso 2: Configurar Servidor Multimedia

Antes de sincronizar usuarios, debes configurar el servidor.

### **Configurar Jellyfin:**
```bash
curl -X POST http://192.168.3.180:5001/api/config/JELLYFIN \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Servidor Jellyfin",
    "baseUrl": "http://192.168.1.100",
    "port": 8096,
    "apiKey": "tu-api-key-de-jellyfin",
    "active": true
  }'
```

### **Configurar Plex:**
```bash
curl -X POST http://192.168.3.180:5001/api/config/PLEX \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Servidor Plex",
    "baseUrl": "http://192.168.1.101",
    "port": 32400,
    "apiKey": "tu-x-plex-token",
    "active": true
  }'
```

### **Configurar Emby:**
```bash
curl -X POST http://192.168.3.180:5001/api/config/EMBY \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Servidor Emby",
    "baseUrl": "http://192.168.1.102",
    "port": 8096,
    "apiKey": "tu-api-key-de-emby",
    "active": true
  }'
```

**Respuesta esperada:**
```json
{
  "id": "clx...",
  "name": "Mi Servidor Jellyfin",
  "type": "JELLYFIN",
  "baseUrl": "http://192.168.1.100",
  "port": 8096,
  "active": true,
  "createdAt": "2025-10-26T00:00:00.000Z",
  "updatedAt": "2025-10-26T00:00:00.000Z"
}
```

---

## 📤 Paso 3: Exportar Usuarios (Ver lista)

### **Exportar de Jellyfin:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/jellyfin/export-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta esperada:**
```json
{
  "estado": "ok",
  "mensaje": "Exportación completada correctamente.",
  "usuarios": [
    {
      "id": "abc123def456",
      "nombre": "Usuario1",
      "ultimoAcceso": "2025-10-25T10:30:00.000Z"
    },
    {
      "id": "xyz789ghi012",
      "nombre": "Usuario2",
      "ultimoAcceso": "2025-10-24T15:45:00.000Z"
    }
  ]
}
```

### **Exportar de Plex:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/plex/export-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta esperada:**
```json
{
  "estado": "ok",
  "mensaje": "Exportación completada correctamente.",
  "usuarios": [
    {
      "id": "12345",
      "nombre": "UsuarioPlex1",
      "email": "usuario1@example.com"
    },
    {
      "id": "67890",
      "nombre": "UsuarioPlex2",
      "email": "usuario2@example.com"
    }
  ]
}
```

### **Exportar de Emby:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/emby/export-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## 📥 Paso 4: Importar Usuarios (Sincronizar al panel)

### **Importar de Jellyfin:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/jellyfin/import-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta esperada:**
```json
{
  "estado": "ok",
  "mensaje": "Importación completada: 5 usuarios nuevos, 3 ya existían.",
  "importados": 5,
  "omitidos": 3
}
```

### **Importar de Plex:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/plex/import-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### **Importar de Emby:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/emby/import-users \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## ➕ Paso 5: Crear Usuario Nuevo (Jellyfin/Emby)

### **Crear en Jellyfin:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/jellyfin/create-user \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "NuevoUsuario123",
    "password": "Password123!."
  }'
```

**Respuesta esperada:**
```json
{
  "estado": "ok",
  "mensaje": "Usuario creado en Jellyfin y sincronizado con el panel.",
  "usuario": {
    "id": "abc123new",
    "nombre": "NuevoUsuario123"
  }
}
```

### **Crear en Emby:**
```bash
curl -X POST http://192.168.3.180:5001/api/integrations/emby/create-user \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "NuevoUsuarioEmby",
    "password": "Password123!."
  }'
```

---

## 📊 Paso 6: Ver Usuarios Sincronizados

### **Listar todos los usuarios multimedia:**
```bash
curl -X GET "http://192.168.3.180:5001/api/media-users" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### **Filtrar por plataforma:**
```bash
# Solo usuarios de Jellyfin
curl -X GET "http://192.168.3.180:5001/api/media-users?service=JELLYFIN" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Solo usuarios activos de Plex
curl -X GET "http://192.168.3.180:5001/api/media-users?service=PLEX&status=active" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Buscar usuario por nombre
curl -X GET "http://192.168.3.180:5001/api/media-users?search=Usuario1" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta esperada:**
```json
{
  "items": [
    {
      "id": "clx...",
      "displayName": "Usuario1",
      "email": null,
      "externalId": "abc123def456",
      "platform": "JELLYFIN",
      "status": "active",
      "credits": 0,
      "expiresAt": null,
      "createdAt": "2025-10-26T00:00:00.000Z",
      "updatedAt": "2025-10-26T00:00:00.000Z"
    }
  ],
  "meta": {
    "total": 8,
    "page": 1,
    "limit": 50,
    "totalPages": 1,
    "statusBreakdown": [
      { "status": "active", "count": 7 },
      { "status": "inactive", "count": 1 }
    ]
  }
}
```

---

## 🧪 Pruebas con Postman

### **1. Crear colección:**
1. Abre Postman
2. Crea nueva colección "Panelplex API"
3. Agrega variable de entorno:
   - `baseUrl`: `http://192.168.3.180:5001/api`
   - `token`: `TU_TOKEN_JWT`

### **2. Configurar Authorization:**
1. En la colección, ve a: **Authorization**
2. Type: **Bearer Token**
3. Token: `{{token}}`
4. Todos los requests heredarán esta configuración

### **3. Crear requests:**

**Login:**
- Method: `POST`
- URL: `{{baseUrl}}/auth/login`
- Body (JSON):
  ```json
  {
    "email": "admin@mediapanel.local",
    "password": "Admin123!."
  }
  ```

**Exportar Jellyfin:**
- Method: `POST`
- URL: `{{baseUrl}}/integrations/jellyfin/export-users`

**Importar Jellyfin:**
- Method: `POST`
- URL: `{{baseUrl}}/integrations/jellyfin/import-users`

**Crear Usuario:**
- Method: `POST`
- URL: `{{baseUrl}}/integrations/jellyfin/create-user`
- Body (JSON):
  ```json
  {
    "displayName": "TestUser",
    "password": "TestPass123"
  }
  ```

---

## ⚠️ Manejo de Errores

### **401 Unauthorized:**
```json
{
  "statusCode": 401,
  "message": "Unauthorized"
}
```
**Solución:** Token expirado o inválido. Vuelve a hacer login.

### **404 Not Found:**
```json
{
  "statusCode": 404,
  "message": "No hay un servidor Jellyfin configurado."
}
```
**Solución:** Configura el servidor primero (Paso 2).

### **400 Bad Request:**
```json
{
  "statusCode": 400,
  "message": "El servidor Jellyfin está marcado como inactivo."
}
```
**Solución:** Activa el servidor en la configuración.

### **Error de conexión:**
```json
{
  "statusCode": 400,
  "message": "No fue posible conectarse a Jellyfin: Connection timeout"
}
```
**Solución:** Verifica que la URL y puerto del servidor sean correctos.

---

## 🔍 Debugging

### **Ver logs del backend:**
```bash
docker compose logs backend -f
```

### **Verificar configuración de servidores:**
```bash
# Listar todos los servidores configurados
curl -X GET http://192.168.3.180:5001/api/config \
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Ver servidor específico
curl -X GET http://192.168.3.180:5001/api/config/JELLYFIN \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### **Probar conexión a servidor:**
```bash
curl -X POST http://192.168.3.180:5001/api/config/JELLYFIN/test \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta exitosa:**
```json
{
  "estado": "ok",
  "mensaje": "Conexión exitosa",
  "detalles": {
    "codigoHttp": 200,
    "url": "http://192.168.1.100:8096",
    "servicio": "JELLYFIN"
  }
}
```

---

## 📝 Notas Importantes

### **Sobre Jellyfin y Emby:**
- Requieren API Key con permisos de administrador
- La API Key se encuentra en: **Dashboard > API Keys**
- El header debe ser: `X-Emby-Token: tu-api-key`

### **Sobre Plex:**
- Requiere X-Plex-Token (encontrado en URL al iniciar sesión)
- No soporta creación directa de usuarios locales
- Solo importa usuarios compartidos/amigos

### **Prevención de Duplicados:**
- El sistema usa `externalId` para identificar usuarios únicos
- Al importar, usuarios existentes se omiten automáticamente
- No se crearán duplicados aunque ejecutes import múltiples veces

---

## ✅ Checklist de Pruebas

- [ ] Login exitoso y obtención de token
- [ ] Configuración de servidor Jellyfin/Plex/Emby
- [ ] Prueba de conexión al servidor exitosa
- [ ] Exportar usuarios retorna lista correcta
- [ ] Importar usuarios sincroniza al panel
- [ ] Crear usuario funciona en Jellyfin/Emby
- [ ] Ver usuarios sincronizados en `/api/media-users`
- [ ] Filtros por plataforma funcionan
- [ ] Búsqueda por nombre funciona

---

🎉 **¡Sistema de sincronización completamente funcional!**

**Próximo paso:** Integrar botones en el frontend para estas operaciones.
