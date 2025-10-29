# 🚀 Inicio Rápido - Sistema de Paquetes

## ✅ Todo está listo

Los contenedores están corriendo. Accede ahora mismo:

**URL:** http://192.168.3.180:5174  
**Usuario:** admin@mediapanel.local  
**Password:** Admin123!.

## 📦 Nueva Funcionalidad: Paquetes con Bibliotecas Reales

### ¿Qué hace?
Conecta con tu servidor Jellyfin/Plex/Emby, obtiene las bibliotecas reales y te permite crear paquetes seleccionando bibliotecas con checkboxes.

### Usar en 3 pasos:

**1. Configurar servidor (solo primera vez)**
```
Menú: Servidores → Jellyfin
URL: http://tu-servidor:8096
API Key: [obtener desde Jellyfin Dashboard → API Keys]
Guardar
```

**2. Crear paquete**
```
Menú: Paquetes Jellyfin → Nuevo paquete
Sistema carga bibliotecas automáticamente
Seleccionar las que quieras
Nombre: "Full Películas"
Guardar
```

**3. ¡Listo!**
```
El paquete está creado
Pronto podrás asignarlo a usuarios
```

## 📚 Documentación Completa

| Lee esto si... | Archivo |
|----------------|---------|
| Quieres usar el sistema | **GUIA-USO-PAQUETES.md** |
| Necesitas detalles técnicos | **IMPLEMENTACION-PAQUETES-JELLYFIN.md** |
| Quieres ver resumen ejecutivo | **RESUMEN-EJECUTIVO-PAQUETES.md** |
| Quieres contexto completo | **SESION-COMPLETA-2025-10-26.md** |

## 🔧 Comandos Básicos

```bash
# Ver estado
cd /root/Panelplex
docker compose ps

# Ver logs
docker compose logs -f backend

# Reiniciar
docker compose restart backend frontend

# Reconstruir (después de cambios de código)
docker compose down
docker compose up -d --build
```

## 🎯 Siguiente Paso Sugerido

**Implementar asignación de paquetes a usuarios**

Al crear un usuario, seleccionar paquetes → el sistema asigna automáticamente las bibliotecas en Jellyfin/Plex/Emby.

## 🆘 Solución Rápida de Problemas

**No cargan bibliotecas:**
1. Ir a Servidores
2. Configurar Jellyfin primero
3. Probar conexión
4. Volver a Paquetes

**Error de conexión:**
- Verificar URL del servidor
- Verificar API Key
- Ver logs: `docker compose logs backend`

**Cambios no se ven:**
```bash
docker compose down
docker compose up -d --build
# Esperar 1 minuto
# Refrescar navegador (Ctrl+F5)
```

## 🎉 ¡Empieza Ahora!

Todo está configurado y funcionando. Solo necesitas:

1. Abrir http://192.168.3.180:5174
2. Login
3. Ir a "Servidores" y configurar Jellyfin
4. Ir a "Paquetes Jellyfin" y crear tu primer paquete

**¡Es así de simple!**

---

**Versión:** 2.0.0  
**Estado:** ✅ Producción Ready  
**Última actualización:** 26/10/2025
