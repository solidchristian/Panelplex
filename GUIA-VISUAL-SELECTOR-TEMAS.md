# 🔍 GUÍA VISUAL: Dónde está el icono del Selector de Temas

## Vista Desktop (pantalla grande)

```
╔════════════════════════════════════════════════════════════════════════════════╗
║  BARRA SUPERIOR (Topbar)                                                       ║
║                                                                                 ║
║  ☰  Panel principal                               [🎨]  Admin Usuario          ║
║      Administración centralizada                   ↑     (ADMIN)               ║
║                                                     │                           ║
║                                              EL ICONO ESTÁ AQUÍ                 ║
║                                              (botón redondo con                 ║
║                                               icono de paleta)                  ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║  CONTENIDO DEL DASHBOARD                                                       ║
║                                                                                 ║
║  [Tarjetas de contenido, estadísticas, etc...]                                ║
║                                                                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

## Vista Móvil (pantalla pequeña)

```
╔═══════════════════════════════════╗
║  ☰  Panel principal      [🎨] 👤  ║
║                           ↑        ║
║                    ICONO AQUÍ      ║
╠═══════════════════════════════════╣
║                                    ║
║  Contenido...                     ║
║                                    ║
╚═══════════════════════════════════╝
```

## Cómo se ve el botón del selector de temas:

```
┌─────────────────────────────────────────┐
│ Antes de hacer clic:                    │
│                                          │
│   ╭───────╮                             │
│   │   🎨  │  <- Botón circular          │
│   ╰───────╯     con borde              │
│                                          │
│ Color: Fondo blanco/superficie          │
│ Borde: Color del tema                   │
│ Hover: Se agranda ligeramente           │
└─────────────────────────────────────────┘
```

## Al hacer clic en el botón 🎨:

```
                                    ╭─────────────────────────────────╮
                                    │  🎨 Selecciona un tema          │
                                    │  Elige el estilo visual         │
                                    ├─────────────────────────────────┤
                                    │  CORPORATIVO                    │
                                    │  ┌──────────────────────────┐  │
                                    │  │ ☑️ Corporate Light       │  │ <- Seleccionado
                                    │  │    Modo claro            │  │
                                    │  └──────────────────────────┘  │
                                    │  ┌──────────────────────────┐  │
                                    │  │ ☐  Corporate Dark        │  │
                                    │  │    Modo oscuro           │  │
                                    │  └──────────────────────────┘  │
                                    │                                 │
                                    │  BANCARIO                       │
                                    │  ┌──────────────────────────┐  │
                                    │  │ ☐  Banking Light         │  │
                                    │  │    Modo claro            │  │
                                    │  └──────────────────────────┘  │
                                    │  ┌──────────────────────────┐  │
                                    │  │ ☐  Banking Dark          │  │
                                    │  │    Modo oscuro           │  │
                                    │  └──────────────────────────┘  │
                                    │                                 │
                                    │  OCÉANO                         │
                                    │  ┌──────────────────────────┐  │
                                    │  │ ☐  Ocean Light           │  │
                                    │  │    Modo claro            │  │
                                    │  └──────────────────────────┘  │
                                    ╰─────────────────────────────────╯
```

## Características visuales del botón:

1. **Tamaño**: 40x40px (h-10 w-10)
2. **Forma**: Circular redondeada (rounded-xl)
3. **Icono**: Paleta de pintor (Palette de lucide-react)
4. **Color del icono**: Color de acento del tema actual
5. **Animaciones**:
   - Hover: Se agranda un 5% (scale: 1.05)
   - Click: Se reduce ligeramente (scale: 0.92)
   - El icono rota 12° al hacer hover

## Si NO VES el icono 🎨:

### Opción 1: Verificar en DevTools
1. Presiona **F12** en tu navegador
2. Ve a la pestaña **Elements** o **Inspeccionar**
3. Busca en el código HTML: `<button` con `aria-label="Selector de tema"`
4. Si existe en el HTML pero no lo ves, puede ser un problema de CSS/Z-index

### Opción 2: Verificar la consola
1. Presiona **F12** → pestaña **Console**
2. Busca errores en rojo
3. Errores comunes:
   - "Cannot find module 'lucide-react'"
   - "Palette is not defined"
   - Errores de importación

### Opción 3: Forzar recarga
1. Presiona **Ctrl + Shift + R** (o **Cmd + Shift + R** en Mac)
2. Esto recarga la página ignorando la caché
3. El icono debería aparecer

### Opción 4: Verificar que estás logueado
- El icono solo aparece cuando estás dentro del panel
- URL correcta: `http://192.168.3.180:5174`
- Debes haber iniciado sesión primero

## Código relevante:

El componente se encuentra en:
```
/root/Panelplex/packages/frontend/src/components/common/theme-selector.tsx
```

Y se usa en:
```
/root/Panelplex/packages/frontend/src/components/navigation/topbar.tsx
```

En la línea 32 del Topbar:
```tsx
<ThemeSelector />
```

## Estados del botón:

- **Normal**: Borde gris, fondo blanco
- **Hover**: Borde color de acento, fondo con acento al 10%
- **Activo**: Panel desplegable visible
- **Disabled**: No aplica (siempre está habilitado)

## Posición en el DOM:

```html
<div class="flex h-16 items-center justify-between ...">  <!-- Topbar -->
  <div class="flex items-center gap-3">...</div>          <!-- Izquierda -->
  <div class="flex items-center gap-3">                   <!-- Derecha -->
    <div class="relative">                                <!-- ThemeSelector -->
      <button type="button" ...>                          <!-- Botón del selector -->
        <svg>...</svg>                                    <!-- Icono Palette -->
      </button>
    </div>
    <div>...</div>                                        <!-- Info usuario -->
  </div>
</div>
```
