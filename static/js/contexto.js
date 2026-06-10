const ESTADO = {
    idSesion: SESION.id_sesion,
    maxIntentos: SESION.max_intentos,
    juegoTerminado: false,
    cantidadIntentos: 0,
    mejorScore: null
};

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("label-tematica").textContent = `Temática: ${SESION.tematica}`;
    document.getElementById("input-palabra").addEventListener("keydown", e => {
        if (e.key === "Enter") confirmarIntento();
    });

    if (SESION.intentos_ordenados && SESION.intentos_ordenados.length > 0) {
        SESION.intentos_ordenados.forEach(i => renderizarIntento(i.palabra, i.similitud, false));
        actualizarMetricas(SESION.cantidad_intentos);
    }
});

async function confirmarIntento() {
    if (ESTADO.juegoTerminado) return;

    const input = document.getElementById("input-palabra");
    const intento = input.value.trim().toLowerCase();

    ocultarError();

    if (!intento) return;

    try {
        const res = await fetch("/juegos/contexto/intento", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_sesion: ESTADO.idSesion, intento })
        });

        const data = await res.json();

        if (data.error) {
            mostrarError(data.error);
            return;
        }

        input.value = "";
        input.focus();

        actualizarMetricas(data.cantidad_intentos);
        document.getElementById("score-valor").textContent = data.puntaje;

        if (data.estado === "ganada") {
            ESTADO.juegoTerminado = true;
            setTimeout(() => mostrarResultado(data), 400);
        } else {
            renderizarListaCompleta(data.intentos_ordenados);
            if (data.estado === "perdida") {
                ESTADO.juegoTerminado = true;
                setTimeout(() => mostrarResultado(data), 800);
            }
        }

    } catch(err) {
        mostrarError("Error de conexión. Intentá de nuevo.");
    }
}

async function rendirse() {
    if (ESTADO.juegoTerminado) return;

    try {
        const res = await fetch("/juegos/contexto/rendirse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_sesion: ESTADO.idSesion })
        });

        const data = await res.json();

        if (data.error) {
            mostrarError(data.error);
            return;
        }

        ESTADO.juegoTerminado = true;
        mostrarResultado({ estado: "rendida", palabra: data.palabra, puntaje: 0 });

    } catch {
        mostrarError("Error de conexión. Intentá de nuevo.");
    }
}

function renderizarListaCompleta(intentos) {
    const lista = document.getElementById("lista-intentos");
    lista.innerHTML = "";
    intentos.forEach((item, index) => {
        renderizarIntento(item.palabra, item.similitud, index === 0);
    });
}

function renderizarIntento(palabra, similitud, esPrimero) {
    const lista = document.getElementById("lista-intentos");

    const item = document.createElement("div");
    item.className = "contexto-item" + (esPrimero ? " top-item" : "") + (similitud === 1 ? " ganador" : "");

    const anchoBarra = Math.max(4, Math.round((1 - (similitud - 1) / 99) * 100));
    const color = colorPorScore(similitud);

    item.innerHTML = `
        <span class="contexto-item-palabra">${palabra.toUpperCase()}</span>
        <div class="contexto-item-derecha">
            <div class="contexto-barra-container">
                <div class="contexto-barra" style="width: ${anchoBarra}%; background: ${color};"></div>
            </div>
            <span class="contexto-score">${similitud}</span>
        </div>
    `;

    lista.appendChild(item);
}

function colorPorScore(similitud) {
    if (similitud <= 5)  return "#10B981";
    if (similitud <= 20) return "#34D399";
    if (similitud <= 40) return "#FCD34D";
    if (similitud <= 70) return "#F97316";
    return "#EF4444";
}

function actualizarMetricas(cantidadIntentos) {
    ESTADO.cantidadIntentos = cantidadIntentos;

    document.getElementById("contador-intentos").textContent = `${cantidadIntentos} / ${ESTADO.maxIntentos}`;
    
    document.getElementById("barra-intentos").style.setProperty(
        "--dynamic-width",
        `${(cantidadIntentos / ESTADO.maxIntentos) * 100}%`
    );

    const lista = document.getElementById("lista-intentos");
    const primerItem = lista.querySelector(".contexto-score");
    if (primerItem) {
        document.getElementById("metrica-mejor").textContent = primerItem.textContent;
    }
}



function mostrarResultado(data) {
    document.querySelector("main.wordle-container").style.display = "none";
    const pantalla = document.getElementById("pantalla-resultado");
    pantalla.classList.add("visible");

    const gano = data.estado === "ganada";
    const rendido = data.estado === "rendida";
    

    document.getElementById("resultado-titulo").textContent = gano ? "¡Ganaste!" : rendido ? "Te rendiste" : "¡Perdiste!";
    document.getElementById("resultado-palabra").textContent = gano
    ? `¡Adivinaste la palabra! Era: ${data.palabra.toUpperCase()}`
    : `La palabra era: ${data.palabra.toUpperCase()}`;


    if (!USUARIO_LOGUEADO) {
        if (!document.getElementById("aviso-invitado")) {
            const aviso = document.createElement("div");
            aviso.id = "aviso-invitado";
            aviso.className = "metric-card aviso-invitado-box";
            aviso.innerHTML = `
                <h3 class="metric-card-title">MODO INVITADO</h3>
                <p class="result-word aviso-separador">Los puntos de esta partida no se guardaron en el sistema.</p>
                <a href="/auth/login" class="navbar-btn">Iniciar Sesión</a>
            `;
            const boton = pantalla.querySelector("button");
            pantalla.insertBefore(aviso, boton);
        }
    }
}

function mostrarError(msg) {
    const el = document.getElementById("error-juego");
    el.textContent = msg;
    el.classList.add("visible");
}

function ocultarError() {
    document.getElementById("error-juego").classList.remove("visible");
}