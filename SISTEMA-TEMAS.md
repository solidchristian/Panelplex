# Sistema de Temas Múltiples - Panelplex MediaPanel

## 📋 Resumen de Cambios

Se ha implementado un **sistema completo de temas** con 10 temas profesionales (5 estilos x 2 modos: claro/oscuro) inspirados en sitios corporativos modernos como MetLife, Banco Chile y Banco Estado.

## 🎨 Temas Disponibles

### 1. **Corporate (Estilo MetLife)**
- **Corporate Light** - Tema claro corporativo con azul profesional (#0066cc)
- **Corporate Dark** - Tema oscuro corporativo elegante

### 2. **Banking (Estilo Banco Chile/Estado)**
- **Banking Light** - Tema bancario claro con azules institucionales (#2874a6)
- **Banking Dark** - Tema bancario oscuro profesional

### 3. **Ocean**
- **Ocean Light** - Tema claro con tonos azul cielo (#0ea5e9)
- **Ocean Dark** - Tema oscuro con tonos oceánicos profundos

### 4. **Modern (Tech Style)**
- **Modern Light** - Tema moderno claro con púrpura (#8b5cf6)
- **Modern Dark** - Tema moderno oscuro tecnológico

### 5. **Minimal (Clean Style)**
- **Minimal Light** - Tema minimalista claro monocromático
- **Minimal Dark** - Tema minimalista oscuro elegante

## 🚀 Características Implementadas

### ✅ Sistema de Variables CSS
Cada tema define variables CSS personalizadas:
- `--theme-bg` - Color de fondo principal
- `--theme-surface` - Color de superficie (cards, panels)
- `--theme-foreground` - Color de texto principal
- `--theme-accent` - Color de acento principal
- `--theme-border` - Color de bordes
- `--theme-muted` - Color de texto secundario
- Y más...

### ✅ Selector de Temas Interactivo
- Botón con ícono de paleta en la barra superior
- Panel desplegable organizado por categorías
- Vista previa visual de cada tema
- Indicador del tema activo
- Animaciones suaves con Framer Motion

### ✅ Persistencia
- Los temas se guardan en `localStorage`
- Se mantienen al recargar la página
- Configuración inicial por defecto: Corporate Light

### ✅ Componentes Actualizados
Todos los componentes principales ahora usan variables de tema:
- ✅ Layout principal
- ✅ Sidebar (navegación lateral)
- ✅ Topbar (barra superior)
- ✅ Auth Panel (panel de autenticación)
- ✅ Theme Selector (selector de temas)

## 📁 Archivos Modificados/Creados

### Nuevos Archivos
```
src/components/common/theme-selector.tsx          - Componente selector de temas
src/components/providers/theme-provider.tsx      - Proveedor de contexto (actualizado)
```

### Archivos Modificados
```
src/app/globals.css                              - Definición de 10 temas CSS
src/app/layout.tsx                               - Script de carga inicial
src/components/navigation/topbar.tsx             - Integración del selector
src/components/navigation/sidebar.tsx            - Uso de variables tema
src/components/dashboard/auth-panel.tsx          - Uso de variables tema
```

### Archivos Eliminados
```
src/components/common/theme-toggle.tsx           - Reemplazado por theme-selector
```

## 🎯 Cómo Usar

### Para los Usuarios
1. Hacer clic en el ícono de paleta (🎨) en la barra superior derecha
2. Seleccionar un tema de la lista organizada por categorías
3. El tema se aplica inmediatamente con transiciones suaves
4. El tema seleccionado se guarda automáticamente

### Para Desarrolladores

#### Usar Variables de Tema en Componentes
```tsx
// En lugar de colores hardcodeados:
className="bg-white text-gray-900 border-gray-200"

// Usar variables de tema:
className="bg-theme-surface text-theme-foreground border-theme-border"
```

#### Clases Utility Disponibles
```css
/* Backgrounds */
.bg-theme-bg
.bg-theme-surface
.bg-theme-card
.bg-theme-hover
.bg-theme-accent
.bg-theme-accent/10

/* Text */
.text-theme-foreground
.text-theme-muted
.text-theme-accent

/* Borders */
.border-theme-border
.border-theme-accent
```

#### Usar el Hook useTheme
```tsx
import { useTheme } from '@/components/providers/theme-provider';

function MyComponent() {
  const { theme, setTheme, themes, currentMode } = useTheme();
  
  // Cambiar tema programáticamente
  setTheme('ocean-dark');
  
  // Obtener modo actual
  console.log(currentMode); // 'light' o 'dark'
  
  // Listar todos los temas
  console.log(themes);
}
```

## 🎨 Paletas de Colores por Tema

### Corporate Light
```css
Fondo: #ffffff
Acento: #0066cc (Azul corporativo)
Texto: #1a1a1a
```

### Banking Light
```css
Fondo: #fafbfc
Acento: #2874a6 (Azul bancario)
Texto: #2c3e50
```

### Ocean Light
```css
Fondo: #f0f9ff
Acento: #0ea5e9 (Azul cielo)
Texto: #0c4a6e
```

### Modern Light
```css
Fondo: #fafafa
Acento: #8b5cf6 (Púrpura moderno)
Texto: #18181b
```

### Minimal Light
```css
Fondo: #ffffff
Acento: #404040 (Gris neutro)
Texto: #171717
```

## 🔧 Agregar un Nuevo Tema

### Paso 1: Definir en theme-provider.tsx
```tsx
export type ThemeName = 'mi-nuevo-tema-light' | 'mi-nuevo-tema-dark' | ...;

export const AVAILABLE_THEMES: ThemeConfig[] = [
  { id: 'mi-nuevo-tema-light', name: 'Mi Tema Claro', mode: 'light', category: 'Mi Categoría' },
  { id: 'mi-nuevo-tema-dark', name: 'Mi Tema Oscuro', mode: 'dark', category: 'Mi Categoría' },
  ...
];
```

### Paso 2: Definir CSS en globals.css
```css
.mi-nuevo-tema-light {
  --theme-bg: #...;
  --theme-foreground: #...;
  --theme-accent: #...;
  --theme-border: #...;
  --theme-muted: #...;
  /* ... más variables ... */
  color-scheme: light;
}

.mi-nuevo-tema-dark {
  /* ... versión oscura ... */
  color-scheme: dark;
}
```

## ✅ Testing

### Build Exitoso
```bash
cd /root/Panelplex/packages/frontend
npm run build
```
✅ Compilación exitosa sin errores TypeScript

### Iniciar Servidor de Desarrollo
```bash
cd /root/Panelplex/packages/frontend
npm run dev
```
Luego abrir http://localhost:3000

## 🎯 Funcionalidades del Sistema

### ✅ Completadas
- [x] 10 temas profesionales (5 estilos x 2 modos)
- [x] Selector visual interactivo
- [x] Persistencia en localStorage
- [x] Variables CSS dinámicas
- [x] Transiciones suaves
- [x] Componentes actualizados
- [x] Sistema completamente tipado (TypeScript)
- [x] Organización por categorías
- [x] Preview visual de temas

### 🔮 Mejoras Futuras Posibles
- [ ] Tema personalizable por usuario
- [ ] Editor de colores en tiempo real
- [ ] Temas por servidor (Plex/Emby/Jellyfin)
- [ ] Exportar/importar configuraciones de tema
- [ ] Modo automático según hora del día
- [ ] Temas de alto contraste (accesibilidad)

## 📝 Notas de Autenticación

El sistema de autenticación sigue funcionando con las mismas credenciales:
- **Email**: admin@mediapanel.local
- **Password**: Admin123!

El panel de autenticación ahora se adapta a todos los temas automáticamente.

## 🚦 Próximos Pasos

1. **Iniciar el servidor de desarrollo**:
   ```bash
   cd /root/Panelplex/packages/frontend
   npm run dev
   ```

2. **Probar los temas**:
   - Hacer login con las credenciales
   - Hacer clic en el ícono de paleta
   - Probar cada tema y verificar la funcionalidad

3. **Verificar el backend**:
   ```bash
   cd /root/Panelplex/packages/backend
   npm run start:dev
   ```

4. **Continuar desarrollo**:
   - Aplicar variables de tema a componentes adicionales
   - Agregar más funcionalidades al panel
   - Integrar con servicios de media (Plex/Emby/Jellyfin)

## 💡 Recordatorio para Continuar

Si sales de la sesión con Ctrl+C, para continuar usa:

```bash
# Desde cualquier directorio
cd /root/Panelplex

# Ver este documento
cat packages/frontend/SISTEMA-TEMAS.md

# O simplemente decir a Copilot:
"Continuemos con el proyecto Panelplex, implementa [siguiente funcionalidad]"
```

El sistema de temas está completamente funcional y listo para usar. Todos los cambios están guardados y el proyecto compila exitosamente.
