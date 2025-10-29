# ⚡ Referencia Rápida - Panelplex

## 🎯 Acceso Inmediato

### URL de Acceso
```
http://192.168.3.180:5174
```

### Credenciales de Prueba
```
Usuario:    admin@mediapanel.local
Contraseña: Admin123!
```

---

## 🚀 Comandos Esenciales

### ▶️ Iniciar Servidor
```bash
cd /root/Panelplex/packages/frontend
PORT=5174 npm run dev
```

### ⏹️ Detener Servidor
```bash
pkill -f "next dev"
```

### 🔄 Reiniciar (si hay problemas)
```bash
cd /root/Panelplex/packages/frontend
pkill -f "next dev"
rm -rf .next/dev/lock
PORT=5174 npm run dev
```

### 📊 Verificar Estado
```bash
netstat -tlnp | grep 5174
```

---

## 📚 Documentación Disponible

1. **ESTADO-ACTUAL.md** - Estado completo del proyecto
2. **GUIA-TEMAS.md** - Catálogo visual de temas
3. **REFERENCIA-RAPIDA.md** - Este documento
4. **README.md** - Documentación técnica completa

---

## 🎨 Sistema de Temas (10 Temas)

### Acceder al Selector
1. Haz clic en el icono 🎨 (paleta) en el topbar
2. Selecciona tu tema favorito
3. Se guarda automáticamente

### Categorías
- **MetLife Style**: 2 temas (corporativo)
- **Banking Style**: 2 temas (bancario)
- **Modern Style**: 2 temas (oceánico)
- **Tech Style**: 2 temas (moderno)
- **Clean Style**: 2 temas (minimalista)

### Cada categoría tiene
- ☀️ Versión clara (light)
- 🌙 Versión oscura (dark)

---

## 🔧 Resolución de Problemas

### Problema: Página no carga
**Solución:**
```bash
# 1. Verificar que el servidor esté corriendo
netstat -tlnp | grep 5174

# 2. Si no hay output, iniciar servidor
cd /root/Panelplex/packages/frontend
PORT=5174 npm run dev
```

### Problema: Error de lock en Next.js
**Solución:**
```bash
pkill -f "next dev"
rm -rf /root/Panelplex/packages/frontend/.next/dev/lock
cd /root/Panelplex/packages/frontend
PORT=5174 npm run dev
```

### Problema: Puerto ocupado
**Solución:**
```bash
# Liberar puerto 5174
lsof -ti:5174 | xargs kill -9

# Iniciar de nuevo
cd /root/Panelplex/packages/frontend
PORT=5174 npm run dev
```

### Problema: Los temas no cambian
**Verificar:**
- El selector está en el topbar (esquina superior derecha)
- Haz clic en el icono 🎨
- Los cambios son instantáneos
- Se guardan en localStorage

### Problema: No puedo iniciar sesión
**Verificar:**
- Usuario: `admin@mediapanel.local`
- Contraseña: `Admin123!` (con mayúsculas y símbolo)
- El backend debe estar corriendo (puerto 3000)

---

## 📁 Estructura de Archivos Clave

```
/root/Panelplex/
├── packages/frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx          # Layout principal
│   │   │   ├── globals.css         # 10 temas CSS
│   │   │   └── (panel)/            # Rutas del panel
│   │   ├── components/
│   │   │   ├── providers/
│   │   │   │   ├── theme-provider.tsx    # Gestor de temas
│   │   │   │   └── auth-provider.tsx     # Autenticación
│   │   │   ├── common/
│   │   │   │   └── theme-selector.tsx    # Selector visual
│   │   │   └── navigation/
│   │   │       ├── topbar.tsx            # Barra superior
│   │   │       └── sidebar.tsx           # Menú lateral
│   │   └── lib/
│   └── package.json
└── [Documentación]
    ├── ESTADO-ACTUAL.md
    ├── GUIA-TEMAS.md
    └── REFERENCIA-RAPIDA.md
```

---

## 💡 Tips y Trucos

### Desarrollo Rápido
- Los cambios en código se reflejan automáticamente (Hot Reload)
- El tema seleccionado persiste entre recargas
- Usa Ctrl+Shift+I para abrir DevTools

### Cambiar Puerto
```bash
# En lugar de 5174, usa otro puerto
PORT=8080 npm run dev
```

### Ver Logs en Tiempo Real
```bash
tail -f /tmp/frontend.log
```

### Limpiar Caché de Next.js
```bash
cd /root/Panelplex/packages/frontend
rm -rf .next
npm run dev
```

---

## 🎯 Próximas Funcionalidades Sugeridas

1. **Integración de APIs**
   - Plex Media Server
   - Emby Server
   - Jellyfin Server

2. **Dashboard**
   - Estadísticas en tiempo real
   - Gráficos de uso
   - Monitoreo de servidores

3. **Gestión**
   - Usuarios y permisos
   - Bibliotecas multimedia
   - Paquetes y planes

4. **Notificaciones**
   - Toast messages
   - Alertas en tiempo real
   - WebSocket integration

---

## 📞 Cómo Retomar el Proyecto

### Al salir con Ctrl+C
1. El servidor se detiene
2. Los cambios están guardados
3. Para reiniciar:
   ```bash
   cd /root/Panelplex/packages/frontend
   PORT=5174 npm run dev
   ```

### En una nueva sesión de terminal
```bash
# 1. Ver estado del proyecto
cat /root/Panelplex/ESTADO-ACTUAL.md

# 2. Ir al directorio
cd /root/Panelplex/packages/frontend

# 3. Iniciar servidor
PORT=5174 npm run dev

# 4. Abrir en navegador
# http://192.168.3.180:5174
```

### Con GitHub Copilot
Solo di:
- "Muéstrame el estado de Panelplex"
- "Inicia el servidor de Panelplex"
- "Continuemos desarrollando Panelplex"

---

## ✅ Checklist de Verificación

Antes de empezar a trabajar, verifica:

- [ ] Servidor corriendo en puerto 5174
- [ ] Puedes acceder a http://192.168.3.180:5174
- [ ] Puedes iniciar sesión con las credenciales
- [ ] El selector de temas funciona (icono 🎨)
- [ ] Los temas cambian correctamente
- [ ] El sidebar es responsive
- [ ] La navegación funciona

---

## 🌟 Estado Actual

✅ **Servidor**: Activo en puerto 5174  
✅ **Temas**: 10 temas funcionando perfectamente  
✅ **Autenticación**: Implementada con JWT  
✅ **UI/UX**: Diseño moderno y responsive  
✅ **Navegación**: Sidebar y topbar funcionales  
✅ **Persistencia**: localStorage para temas  

**El proyecto está listo para desarrollo continuo** 🚀

---

**Última actualización**: 2025-10-25  
**Versión**: 0.1.0  
**Status**: ✅ Producción OK
