# Mejoras Implementadas: Sistema de Créditos y Gestión de Usuarios

## Resumen de Cambios

Se han implementado las siguientes funcionalidades mejoradas en el sistema de gestión de usuarios multimedia:

---

## 1. Sistema de Créditos (1 crédito = 1 mes)

### Backend: Endpoint para agregar créditos
**Archivo:** `packages/backend/src/media-users/media-users.controller.ts`

```typescript
@Post(':id/add-credits')
@Roles(Role.ADMIN, Role.RESELLER)
addCredits(@Param('id') id: string, @Body() dto: { credits: number })
```

### Lógica implementada:
- Cuando agregas créditos, automáticamente se calcula la nueva fecha de expiración
- **1 crédito = 1 mes** adicional
- Si la cuenta ya expiró, comienza desde la fecha actual
- Si aún no expira, suma los meses a la fecha de expiración existente
- Al agregar créditos, el estado del usuario se cambia automáticamente a "active"

### Ejemplo:
```
Usuario tiene expiresAt: 2025-12-01
Agregas 3 créditos
Nueva expiresAt: 2026-03-01 (3 meses adicionales)
```

---

## 2. Selección Múltiple de Usuarios

### Frontend: Checkbox para selección
- Checkbox en el encabezado para seleccionar/deseleccionar todos
- Checkbox individual por cada usuario
- Contador visual de usuarios seleccionados
- Botón de eliminación múltiple aparece solo cuando hay usuarios seleccionados

### Estado manejado con:
```typescript
const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
```

---

## 3. Opciones de Eliminación Flexible

### Tres opciones de eliminación:
1. **Panel y Servidor** (both) - Elimina el usuario del panel y del servidor multimedia
2. **Solo del Panel** (panel) - Elimina solo del panel, conserva en el servidor
3. **Solo del Servidor** (server) - Elimina del servidor pero mantiene registro en el panel

### Backend: Endpoint mejorado
**Archivo:** `packages/backend/src/media-users/media-users.controller.ts`

```typescript
@Delete(':id')
@Roles(Role.ADMIN)
remove(@Param('id') id: string, @Query('deleteFrom') deleteFrom?: 'panel' | 'server' | 'both')
```

### Endpoint de eliminación múltiple:
```typescript
@Post('bulk-delete')
@Roles(Role.ADMIN)
bulkDelete(@Body() dto: { ids: string[]; deleteFrom: 'panel' | 'server' | 'both' })
```

---

## 4. Integración con Servidores Multimedia

### Eliminación de usuarios en Jellyfin/Emby:
**Archivo:** `packages/backend/src/media-users/media-users.service.ts`

```typescript
private async deleteUserFromServer(platform: MediaServerType, externalId: string) {
  // Llama a la API del servidor multimedia para eliminar el usuario
  const endpoint = new URL(`/Users/${externalId}`, baseUrl);
  await fetch(endpoint.toString(), { method: 'DELETE' });
}
```

### Soporte actual:
- ✅ Jellyfin - Eliminación completa via API
- ✅ Emby - Eliminación completa via API
- ⚠️ Plex - Requiere implementación especial (en desarrollo)

---

## 5. Interfaz de Usuario Mejorada

### Nuevos componentes visuales:

#### Botón de Agregar Créditos
```tsx
<button
  onClick={() => openCreditsModal(user.id)}
  className="inline-flex h-8 w-8 items-center justify-center rounded-lg border"
  title="Agregar créditos"
>
  <CreditCard className="h-4 w-4" />
</button>
```

#### Modal de Créditos
- Interfaz clara para ingresar cantidad de créditos
- Muestra "1 Crédito = 1 Mes"
- Cálculo en tiempo real de meses a agregar

#### Selector de usuarios
- Checkbox con iconos CheckSquare/Square de lucide-react
- Diseño consistente con el tema actual
- Feedback visual al seleccionar

---

## 6. Flujo de Trabajo

### Para agregar créditos a un usuario:
1. Click en el icono de tarjeta de crédito (💳)
2. Ingresar cantidad de créditos (1-120)
3. Confirmar
4. El sistema automáticamente:
   - Suma los créditos al contador
   - Calcula nueva fecha de expiración (+N meses)
   - Reactiva el usuario si estaba suspendido

### Para eliminar usuarios múltiples:
1. Seleccionar usuarios con checkbox
2. Click en "Eliminar (N)" donde N es la cantidad seleccionada
3. Elegir opción:
   - 1 = Panel y Servidor
   - 2 = Solo del Panel
   - 3 = Solo del Servidor
4. Confirmar eliminación

---

## 7. Archivos Modificados

### Backend:
- `packages/backend/src/media-users/media-users.controller.ts`
- `packages/backend/src/media-users/media-users.service.ts`
- `packages/backend/src/media-users/media-users.module.ts`

### Frontend:
- `packages/frontend/src/components/dashboard/media-users-view.tsx`
- `packages/frontend/src/stores/media-users-store.ts`

---

## 8. Endpoints API Nuevos

### POST `/media-users/:id/add-credits`
**Body:** `{ "credits": number }`

**Respuesta:**
```json
{
  "status": "ok",
  "message": "3 crédito(s) agregado(s). Nueva fecha de expiración: 2026-03-01T00:00:00.000Z",
  "user": { ... }
}
```

### POST `/media-users/bulk-delete`
**Body:**
```json
{
  "ids": ["id1", "id2", "id3"],
  "deleteFrom": "both" | "panel" | "server"
}
```

**Respuesta:**
```json
{
  "status": "ok",
  "deletedCount": 3,
  "totalRequested": 3,
  "errors": []
}
```

### DELETE `/media-users/:id?deleteFrom=both`
**Query Params:** `deleteFrom` = "both" | "panel" | "server"

---

## 9. Validaciones Implementadas

- Créditos deben ser mayor a 0
- Máximo 120 créditos (10 años)
- Verificación de servidor activo antes de eliminar del servidor
- Manejo de errores si el servidor no está disponible
- Confirmación antes de eliminación múltiple

---

## 10. Próximos Pasos Sugeridos

1. **Historial de créditos**: Tabla de auditoría para ver quién agregó créditos y cuándo
2. **Notificaciones automáticas**: Alertas antes de que expire un usuario
3. **Paquetes de créditos**: Predefinir paquetes (1 mes, 3 meses, 6 meses, 1 año)
4. **Renovación automática**: Opción para auto-renovar usuarios con tarjeta
5. **Dashboard de ventas**: Reportes de créditos vendidos por período

---

## Cómo Probar las Nuevas Funcionalidades

### 1. Agregar créditos:
```bash
# Acceder a http://192.168.3.180:5174
# Ir a Usuarios > Jellyfin/Plex/Emby
# Click en el icono 💳 de cualquier usuario
# Ingresar cantidad de créditos
# Observar la nueva fecha de expiración
```

### 2. Eliminación múltiple:
```bash
# Seleccionar múltiples usuarios con los checkbox
# Click en "Eliminar (N)"
# Elegir opción 1, 2 o 3
# Confirmar
```

### 3. Ver créditos y expiración:
```bash
# En la tabla de usuarios, las columnas "Créditos" y "Expira" muestran la información
```

---

## Documentación Técnica Adicional

### Cálculo de Expiración:
```typescript
const currentExpiry = user.expiresAt || new Date();
const newExpiry = new Date(currentExpiry);

// Si ya expiró, comenzar desde ahora
if (currentExpiry < new Date()) {
  newExpiry.setTime(new Date().getTime());
}

// Agregar los meses según los créditos
newExpiry.setMonth(newExpiry.getMonth() + credits);
```

### Estado del Usuario:
- `active` - Usuario activo con acceso
- `suspended` - Usuario suspendido sin acceso
- `expiring` - Usuario próximo a expirar (útil para alertas)

---

## Comandos Docker

### Reconstruir contenedores:
```bash
cd /root/Panelplex
docker compose down
docker compose up -d --build
```

### Ver logs:
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

---

**Fecha de implementación:** 2025-10-26
**Versión:** 1.0.0
**Estado:** ✅ Implementado y desplegado
