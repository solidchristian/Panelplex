# 📦 Implementación de Paquetes con Bibliotecas de Jellyfin

## ✅ Cambios Realizados

### Backend - Nuevas Funcionalidades

#### 1. **Endpoint para obtener bibliotecas del servidor**
   - **Ruta:** `GET /media-packages/libraries/:service`
   - **Servicios soportados:** Jellyfin, Plex, Emby
   - **Autenticación:** Requiere token JWT con roles ADMIN, RESELLER o SUPPORT

#### 2. **Integración con APIs de servidores multimedia**

**Jellyfin:**
```typescript
GET {baseUrl}/Items?api_key={apiKey}&Recursive=false&IncludeItemTypes=CollectionFolder
Header: X-Emby-Token: {apiKey}
```

**Plex:**
```typescript
GET {baseUrl}/library/sections
Header: X-Plex-Token: {apiKey}
```

**Emby:**
```typescript
GET {baseUrl}/Library/VirtualFolders?api_key={apiKey}
Header: X-Emby-Token: {apiKey}
```

#### 3. **Archivos modificados:**
- `/packages/backend/src/media-packages/media-packages.controller.ts`
  - Agregado endpoint `getLibraries()`
  - Agregado método `ensureType()` para validar servicios

- `/packages/backend/src/media-packages/media-packages.service.ts`
  - Agregado método `fetchLibraries()` - método principal
  - Agregado método `fetchJellyfinLibraries()` - específico para Jellyfin
  - Agregado método `fetchPlexLibraries()` - específico para Plex
  - Agregado método `fetchEmbyLibraries()` - específico para Emby
  - Agregado método `composeUrl()` - construye URLs con puertos

### Frontend - Interfaz de Usuario

#### 1. **Selector visual de bibliotecas**
   - Reemplaza el input de texto manual por un selector de checkboxes
   - Carga automática de bibliotecas al abrir el modal de crear/editar paquete
   - Muestra información de cada biblioteca (nombre y tipo)
   - Contador de bibliotecas seleccionadas

#### 2. **Mejoras en UX:**
   - Indicador de carga mientras se obtienen bibliotecas
   - Mensajes informativos cuando no hay bibliotecas disponibles
   - Scroll automático para listas largas de bibliotecas
   - Validación: requiere al menos una biblioteca seleccionada

#### 3. **Archivos modificados:**
- `/packages/frontend/src/components/dashboard/media-packages-view.tsx`
  - Estado `availableLibraries` - almacena bibliotecas del servidor
  - Estado `loadingLibraries` - indicador de carga
  - Estado `selectedLibraries` - conjunto de bibliotecas seleccionadas (Set)
  - Método `loadLibrariesFromServer()` - obtiene bibliotecas via API
  - Método `toggleLibrary()` - selecciona/deselecciona bibliotecas
  - UI actualizada con checkboxes y diseño visual mejorado

## 🔄 Flujo de Trabajo

### Crear un Paquete con Bibliotecas de Jellyfin

1. **Usuario hace clic en "Nuevo paquete"**
   - Se abre el modal
   - Automáticamente se conecta al servidor configurado
   - Carga las bibliotecas disponibles

2. **Usuario completa el formulario:**
   - Nombre del paquete (ej: "Full Películas")
   - Descripción (opcional)
   - **Selecciona bibliotecas** usando checkboxes:
     - ✅ Películas para Niños
     - ✅ Películas Generales
     - ✅ Películas 4K
   - Marca si el paquete está activo

3. **Usuario guarda:**
   - Validación: al menos una biblioteca seleccionada
   - Se crea el paquete en la base de datos
   - Las bibliotecas se almacenan como array de strings

4. **Uso del paquete:**
   - Al asignar usuarios, se les dan permisos sobre las bibliotecas del paquete
   - Facilita la gestión masiva de permisos

## 🎯 Ejemplo de Uso

### Escenario: Crear paquete "Full Películas"

**Bibliotecas en Jellyfin:**
- Películas Niños
- Películas Generales  
- Películas 4K
- Series
- Anime

**Pasos:**
1. Ir a "Paquetes Jellyfin"
2. Clic en "Nuevo paquete"
3. Nombre: "Full Películas"
4. Descripción: "Acceso completo a todas las películas"
5. Seleccionar:
   - ✅ Películas Niños
   - ✅ Películas Generales
   - ✅ Películas 4K
6. Guardar

**Resultado:**
- Paquete creado con 3 bibliotecas
- Disponible para asignar a usuarios
- Visible en la lista de paquetes

## 🔧 Configuración Requerida

### Antes de usar esta funcionalidad:

1. **Configurar servidor Jellyfin:**
   - Ir a "Servidores" o "Configuración Jellyfin"
   - URL: `http://tu-servidor:8096`
   - API Key: obtenerla desde Jellyfin Dashboard
   - Guardar y probar conexión

2. **Verificar permisos:**
   - Usuario debe tener rol ADMIN o RESELLER
   - API Key debe tener permisos de lectura en Jellyfin

## 📡 Respuesta de API

### GET /media-packages/libraries/jellyfin

**Success (200):**
```json
{
  "libraries": [
    {
      "id": "abc123",
      "name": "Películas 4K",
      "type": "movies",
      "path": "/media/movies-4k"
    },
    {
      "id": "def456",
      "name": "Series",
      "type": "tvshows",
      "path": "/media/series"
    }
  ]
}
```

**Error (404):**
```json
{
  "statusCode": 404,
  "message": "No se encontró configuración para JELLYFIN. Configura el servidor primero."
}
```

**Error (400):**
```json
{
  "statusCode": 400,
  "message": "Error al conectar con Jellyfin: 401 Unauthorized"
}
```

## 🚀 Próximos Pasos

1. **Asignación de paquetes a usuarios:**
   - Al crear/editar usuario, seleccionar paquetes
   - Las bibliotecas del paquete se asignan automáticamente

2. **Sincronización con servidor:**
   - Al asignar paquete, crear permisos en Jellyfin
   - Al quitar paquete, remover permisos

3. **Gestión avanzada:**
   - Clonar paquetes
   - Importar/exportar configuraciones
   - Historial de cambios

## 🐛 Solución de Problemas

### "No se encontraron bibliotecas"
- Verificar que el servidor esté configurado en "Servidores"
- Probar la conexión al servidor
- Verificar que el API Key sea válido
- Revisar que haya bibliotecas creadas en Jellyfin

### "Error al conectar con Jellyfin"
- Verificar URL y puerto
- Verificar firewall/red
- Verificar que Jellyfin esté corriendo
- Revisar logs del backend: `docker compose logs backend`

### "No se pueden seleccionar bibliotecas"
- Verificar que el usuario tenga permisos
- Refrescar la página
- Cerrar y abrir el modal nuevamente

## 📝 Acceso al Panel

**URL:** `http://192.168.3.180:5174`

**Credenciales:**
- Email: `admin@mediapanel.local`
- Password: `Admin123!.`

## ✨ Características Implementadas

- ✅ Conexión con API de Jellyfin
- ✅ Obtención de bibliotecas en tiempo real
- ✅ Selector visual con checkboxes
- ✅ Soporte para Plex y Emby (misma interfaz)
- ✅ Validación de datos
- ✅ Manejo de errores detallado
- ✅ UI responsive y moderna
- ✅ Indicadores de carga
- ✅ Mensajes informativos

## 🔐 Seguridad

- API Keys nunca se exponen en el frontend
- Todas las llamadas requieren autenticación JWT
- Validación de roles en cada endpoint
- Timeout de 5 segundos en conexiones a servidores
- Sanitización de URLs
