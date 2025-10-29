# 🚀 PANELPLEX - GUÍA RÁPIDA

## ⚡ INICIO RÁPIDO

### Iniciar el Proyecto
```bash
cd /root/Panelplex/packages/frontend
npm run dev
```
**URL**: http://localhost:3000

### Credenciales
```
Email:    admin@mediapanel.local
Password: Admin123!
```

---

## 🎨 TEMAS DISPONIBLES

1. **Corporate Light/Dark** - Estilo MetLife (Azul #0066cc)
2. **Banking Light/Dark** - Estilo Bancos (Azul #2874a6)
3. **Ocean Light/Dark** - Moderno (Cielo #0ea5e9)
4. **Modern Light/Dark** - Tech (Púrpura #8b5cf6)
5. **Minimal Light/Dark** - Minimalista (Gris #404040)

**Total: 10 temas** (5 estilos × 2 modos)

---

## 🎯 CÓMO USAR LOS TEMAS

### Como Usuario
1. Clic en 🎨 (esquina superior derecha)
2. Seleccionar tema deseado
3. ¡Listo! Se guarda automáticamente

### Como Desarrollador
```tsx
// Usar variables de tema en componentes
<div className="bg-theme-surface text-theme-foreground border-theme-border">
  <button className="bg-theme-accent hover:bg-theme-accent-hover">
    Click
  </button>
</div>

// Cambiar tema programáticamente
import { useTheme } from '@/components/providers/theme-provider';

const { theme, setTheme } = useTheme();
setTheme('ocean-dark');
```

---

## 📁 ARCHIVOS PRINCIPALES

```
src/
├── app/
│   └── globals.css                          ← 10 temas CSS
├── components/
│   ├── common/
│   │   └── theme-selector.tsx               ← Selector de temas 🎨
│   ├── providers/
│   │   └── theme-provider.tsx               ← Sistema de temas
│   └── navigation/
│       ├── topbar.tsx                       ← Incluye selector
│       └── sidebar.tsx                      ← Usa variables tema
```

---

## 🎨 VARIABLES CSS ÚTILES

### Backgrounds
- `bg-theme-bg` - Fondo principal
- `bg-theme-surface` - Superficie
- `bg-theme-card` - Tarjetas
- `bg-theme-accent` - Color de acento

### Texto
- `text-theme-foreground` - Texto principal
- `text-theme-muted` - Texto secundario
- `text-theme-accent` - Texto de acento

### Bordes
- `border-theme-border` - Borde normal
- `border-theme-accent` - Borde de acento

---

## ✅ BUILD Y DEPLOY

```bash
# Compilar
npm run build

# Iniciar producción
npm start

# Desarrollo
npm run dev
```

---

## 📚 DOCUMENTACIÓN COMPLETA

- `SISTEMA-TEMAS.md` - Documentación técnica detallada
- `RESUMEN-TEMAS.md` - Resumen visual con ejemplos
- `IMPLEMENTACION-COMPLETA.md` - Guía completa de implementación

---

## 💡 PARA CONTINUAR

```bash
cd /root/Panelplex
cat IMPLEMENTACION-COMPLETA.md
```

O decirle a Copilot:
```
"Continuemos con el proyecto Panelplex donde lo dejamos"
```

---

## ✨ ESTADO ACTUAL

- ✅ 10 temas profesionales
- ✅ Selector visual interactivo
- ✅ Persistencia en localStorage
- ✅ Todos los componentes actualizados
- ✅ Build exitoso
- ✅ Documentación completa
- 🚀 Listo para continuar

---

*Panelplex MediaPanel - Sistema de administración multimedia unificado*
