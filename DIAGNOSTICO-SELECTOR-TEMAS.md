# 🔧 Script de Diagnóstico del Selector de Temas

## Copia y pega este código en la consola del navegador (F12 → Console)

### Script 1: Verificar si el ThemeSelector existe en el DOM

```javascript
// Verifica si el botón del selector de temas existe
const themeSelectorButton = document.querySelector('button[aria-label="Selector de tema"]');

if (themeSelectorButton) {
  console.log('✅ El botón del selector de temas EXISTE en el DOM');
  console.log('📍 Posición:', themeSelectorButton.getBoundingClientRect());
  console.log('👁️ Visible:', window.getComputedStyle(themeSelectorButton).display !== 'none');
  console.log('🎨 Estilos:', window.getComputedStyle(themeSelectorButton));
  
  // Resaltar el botón
  themeSelectorButton.style.border = '3px solid red';
  themeSelectorButton.style.boxShadow = '0 0 20px red';
  console.log('🔴 El botón debería estar resaltado en ROJO ahora');
} else {
  console.error('❌ El botón del selector de temas NO existe en el DOM');
  console.log('Buscando componentes alternativos...');
  
  // Buscar por clase
  const paletteIcons = document.querySelectorAll('[class*="Palette"]');
  console.log('Iconos de paleta encontrados:', paletteIcons.length);
  
  // Buscar todos los botones en el topbar
  const topbarButtons = document.querySelectorAll('.flex.h-16 button');
  console.log('Botones en el topbar:', topbarButtons.length);
  topbarButtons.forEach((btn, i) => {
    console.log(`Botón ${i}:`, btn.getAttribute('aria-label') || btn.textContent);
  });
}
```

### Script 2: Forzar apertura del selector de temas

```javascript
// Simular clic en el botón del selector de temas
const themeSelectorButton = document.querySelector('button[aria-label="Selector de tema"]');

if (themeSelectorButton) {
  console.log('🖱️ Haciendo clic en el selector de temas...');
  themeSelectorButton.click();
  setTimeout(() => {
    const dropdown = document.querySelector('[class*="theme"]');
    console.log('Panel desplegable visible:', !!dropdown);
  }, 500);
} else {
  console.error('No se pudo encontrar el botón');
}
```

### Script 3: Listar todos los temas disponibles

```javascript
// Obtener tema actual desde localStorage
const currentTheme = localStorage.getItem('mediapanel-theme');
console.log('🎨 Tema actual:', currentTheme || 'No definido');

// Listar clases del HTML
const htmlClasses = document.documentElement.classList;
console.log('📝 Clases en <html>:', Array.from(htmlClasses));

// Verificar variables CSS
const rootStyles = getComputedStyle(document.documentElement);
console.log('🎨 Variables de tema:');
console.log('  --theme-bg:', rootStyles.getPropertyValue('--theme-bg'));
console.log('  --theme-accent:', rootStyles.getPropertyValue('--theme-accent'));
console.log('  --theme-foreground:', rootStyles.getPropertyValue('--theme-foreground'));
```

### Script 4: Cambiar tema manualmente

```javascript
// Cambiar a un tema específico
function changeTheme(themeName) {
  // Opciones: 'corporate-light', 'corporate-dark', 'banking-light', 'banking-dark', 'ocean-light'
  
  localStorage.setItem('mediapanel-theme', themeName);
  
  // Limpiar clases anteriores
  document.documentElement.classList.remove(
    'corporate-light', 'corporate-dark', 
    'banking-light', 'banking-dark', 
    'ocean-light', 'light', 'dark'
  );
  
  // Agregar nueva clase
  const mode = themeName.includes('dark') ? 'dark' : 'light';
  document.documentElement.classList.add(themeName, mode);
  document.documentElement.setAttribute('data-theme', themeName);
  document.documentElement.style.colorScheme = mode;
  
  console.log(`✅ Tema cambiado a: ${themeName} (${mode})`);
  
  // Recargar página para aplicar completamente
  setTimeout(() => location.reload(), 500);
}

// Ejemplos de uso:
// changeTheme('corporate-light');
// changeTheme('corporate-dark');
// changeTheme('banking-light');
// changeTheme('banking-dark');
// changeTheme('ocean-light');

console.log('💡 Usa: changeTheme("nombre-del-tema") para cambiar el tema');
```

### Script 5: Inyectar el selector de temas si no existe

```javascript
// Si el botón no existe, lo inyectamos temporalmente
if (!document.querySelector('button[aria-label="Selector de tema"]')) {
  console.log('⚠️ El selector no existe, inyectando botón temporal...');
  
  const topbar = document.querySelector('.flex.h-16');
  if (topbar) {
    const buttonHTML = `
      <button 
        onclick="alert('El selector de temas debería estar aquí. Verifica el componente ThemeSelector.')"
        style="
          position: fixed;
          top: 20px;
          right: 20px;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: #0066cc;
          color: white;
          border: 3px solid white;
          box-shadow: 0 4px 20px rgba(0,0,0,0.3);
          cursor: pointer;
          z-index: 9999;
          font-size: 24px;
        "
      >
        🎨
      </button>
    `;
    
    document.body.insertAdjacentHTML('beforeend', buttonHTML);
    console.log('✅ Botón temporal inyectado en la esquina superior derecha');
  }
}
```

## Cómo usar estos scripts:

1. **Abre tu navegador** y ve a: http://192.168.3.180:5174
2. **Presiona F12** para abrir DevTools
3. **Ve a la pestaña Console**
4. **Copia y pega** uno de los scripts anteriores
5. **Presiona Enter** para ejecutar
6. **Lee los mensajes** en la consola

## Interpretación de resultados:

### Si dice "✅ El botón del selector de temas EXISTE":
- El componente está correctamente renderizado
- Busca el borde ROJO en la pantalla
- El icono debería estar visible

### Si dice "❌ El botón del selector de temas NO existe":
- Hay un problema de renderizado
- Verifica los errores en la consola
- Posibles causas:
  - Error de importación
  - Componente no montado
  - Condición que previene el renderizado

## Acciones según el resultado:

### El botón existe pero no lo veo:
```javascript
// Hacer zoom en el botón
const btn = document.querySelector('button[aria-label="Selector de tema"]');
btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
btn.style.transform = 'scale(3)';
btn.style.zIndex = '99999';
```

### El botón no existe:
1. Verifica errores en la consola
2. Revisa que estés en la ruta correcta (dentro del panel)
3. Asegúrate de haber iniciado sesión
4. Recarga la página con Ctrl+Shift+R

## Capturas de pantalla para comparar:

Si el selector funciona correctamente, deberías ver:

1. **Topbar superior** con:
   - Botón de menú hamburguesa (☰) a la izquierda
   - Título "Panel principal" 
   - Botón circular con icono de paleta (🎨) a la derecha
   - Información de usuario a la derecha del botón de paleta

2. **Al hacer clic en 🎨**:
   - Panel desplegable aparece debajo del botón
   - Lista de 5 temas disponibles
   - Tema actual marcado con checkmark (✓)
   - Animación suave al abrir/cerrar
