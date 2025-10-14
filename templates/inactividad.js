// inactividad.js
console.log('inactividad, revisando')
// Establecer el tiempo de inactividad en milisegundos (ejemplo: 5 minutos)
var tiempoInactividad = 5 * 60 * 1000; // 5 minutos en milisegundos
var tiempoUltimaActividad = new Date().getTime();

// Función para restablecer la sesión al realizar alguna actividad
function restablecerSesion() {
    tiempoUltimaActividad = new Date().getTime();
}

// Función para verificar la inactividad y cerrar sesión si es necesario
function verificarInactividad() {
    var tiempoActual = new Date().getTime();
    if (tiempoActual - tiempoUltimaActividad > tiempoInactividad) {
        // Hacer logout si ha pasado el tiempo de inactividad
        window.location.href = '/logout';
    }
}

// Configurar eventos de actividad para restablecer el temporizador
$(document).on('mousemove keydown', function() {
    restablecerSesion();
});

// Configurar un temporizador para verificar la inactividad periódicamente
setInterval(function() {
    verificarInactividad();
}, 1000);
