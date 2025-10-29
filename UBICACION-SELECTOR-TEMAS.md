# 🎨 Ubicación del Selector de Temas

## Dónde está el icono 🎨

El selector de temas está ubicado en la **barra superior (Topbar)** en la esquina superior derecha.

### Ubicación exacta:
```
┌─────────────────────────────────────────────────────────────┐
│  ☰  Panel principal                        🎨  👤 Usuario   │  <- TOPBAR
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Contenido del panel...                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Cómo funciona:

1. **Icono de paleta** (🎨) en la esquina superior derecha
2. Al hacer clic, se abre un panel desplegable
3. El panel muestra 5 temas disponibles:
   - **Corporate Light** (estilo MetLife claro)
   - **Corporate Dark** (estilo MetLife oscuro)
   - **Banking Light** (estilo Banco Chile/Estado claro)
   - **Banking Dark** (estilo Banco Chile/Estado oscuro)
   - **Ocean Light** (tema océano claro)

### Componentes involucrados:

- **ThemeSelector** (`src/components/common/theme-selector.tsx`): El componente del selector
- **Topbar** (`src/components/navigation/topbar.tsx`): Barra superior que contiene el selector (línea 32)
- **ThemeProvider** (`src/components/providers/theme-provider.tsx`): Proveedor de contexto de temas

### Si no ves el icono:

1. **Verifica que estés en la URL correcta**: http://192.168.3.180:5174
2. **Asegúrate de haber iniciado sesión** con:
   - Usuario: `admin@mediapanel.local`
   - Contraseña: `Admin123!.`
3. **Busca en la esquina superior derecha** junto al nombre de usuario
4. **El icono es una paleta** (Palette icon de lucide-react)

### Características del selector:

- ✅ Animación al abrir/cerrar
- ✅ Preview visual de cada tema
- ✅ Muestra el tema activo con un checkmark
- ✅ Guarda tu selección en localStorage
- ✅ Aplicación instantánea del tema
- ✅ Responsive (funciona en móvil y desktop)

### Si el icono no aparece en pantalla:

1. Abre las **DevTools** del navegador (F12)
2. Ve a la pestaña **Console**
3. Busca errores relacionados con `ThemeSelector` o `Palette`
4. Verifica en la pestaña **Elements** que el componente `ThemeSelector` esté en el DOM
