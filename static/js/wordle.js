const ESTADO = {
  idSesion: SESION.id_sesion,
  filaActual: 0,
  columnaActual: 0,
  maxIntentos: SESION.max_intentos,
  largoPalabra: SESION.largo_palabra,
  grilla: [],
  juegoTerminado: false,
  letrasCorrectas: 0,
  totalLetras: 0
};

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("label-tematica").textContent = `Temática: ${SESION.tematica}`;
document.getElementById("label-pista").textContent = "";
  construirGrilla();
  actualizarMetricas(0);
});

function construirGrilla() {
  const tablero = document.getElementById("tablero");
  tablero.innerHTML = "";
  ESTADO.grilla = [];

  for (let f = 0; f < ESTADO.maxIntentos; f++) {
    const fila = [];
    const filaEl = document.createElement("div");
    filaEl.className = "wordle-row";
    filaEl.id = `fila-${f}`;

    for (let c = 0; c < ESTADO.largoPalabra; c++) {
      const celda = document.createElement("div");
      celda.className = "wordle-cell empty";
      filaEl.appendChild(celda);
      fila.push({ el: celda, letra: "" });
    }

    tablero.appendChild(filaEl);
    ESTADO.grilla.push(fila);
  }
}

function manejarTecla(tecla) {
  if (ESTADO.juegoTerminado) return;
  ocultarError();

  if (tecla === "Backspace") {
    borrarLetra();
  } else if (tecla === "Enter") {
    confirmarIntento();
  } else if (/^[A-ZÑa-zñ]$/.test(tecla)) {
    agregarLetra(tecla.toUpperCase());
  }
}

function agregarLetra(letra) {
  if (ESTADO.columnaActual >= ESTADO.largoPalabra) return;
  const celda = ESTADO.grilla[ESTADO.filaActual][ESTADO.columnaActual];
  celda.letra = letra;
  celda.el.textContent = letra;
  celda.el.className = "wordle-cell active";
  ESTADO.columnaActual++;
}

function borrarLetra() {
  if (ESTADO.columnaActual <= 0) return;
  ESTADO.columnaActual--;
  const celda = ESTADO.grilla[ESTADO.filaActual][ESTADO.columnaActual];
  celda.letra = "";
  celda.el.textContent = "";
  celda.el.className = "wordle-cell empty";
}

document.addEventListener("keydown", e => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  manejarTecla(e.key.length === 1 ? e.key.toUpperCase() : e.key);
});

async function confirmarIntento() {
  if (ESTADO.juegoTerminado) return;
  ocultarError();

  if (ESTADO.columnaActual < ESTADO.largoPalabra) {
    mostrarError("La palabra debe tener 5 letras.");
    sacudirFila(ESTADO.filaActual);
    return;
  }

  const palabra = ESTADO.grilla[ESTADO.filaActual].map(c => c.letra).join("");

  try {
    const res = await fetch("/juegos/wordle/intento", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_sesion: ESTADO.idSesion, intento: palabra })
    });

    const data = await res.json();

    if (data.error) {
      mostrarError(data.error);
      return;
    }

    const correctasEstaFila = data.evaluacion.filter(r => r.estado === "correcta").length;
    ESTADO.letrasCorrectas += correctasEstaFila;
    ESTADO.totalLetras += ESTADO.largoPalabra;

    revelarFila(ESTADO.filaActual, data.evaluacion);
    actualizarMetricas(data.intentos_usados);
    document.getElementById("score-valor").textContent = data.puntaje;

    if (data.estado === "ganada" || data.estado === "perdida") {
      ESTADO.juegoTerminado = true;
      setTimeout(() => mostrarResultado(data), 1800);
    } else {
      ESTADO.filaActual++;
      ESTADO.columnaActual = 0;
      document.getElementById("instruccion").textContent =
        `Intentos restantes: ${ESTADO.maxIntentos - data.intentos_usados}`;
    }

  } catch {
    mostrarError("Error de conexión. Intentá de nuevo.");
  }
}

function revelarFila(indiceFila, evaluacion) {
  const fila = ESTADO.grilla[indiceFila];
  evaluacion.forEach((resultado, i) => {
    setTimeout(() => {
      const celda = fila[i].el;
      celda.classList.add("flip");
      setTimeout(() => {
        celda.className = `wordle-cell completed estado-${resultado.estado}`;
      }, 250);
    }, i * 120);
  });
}

function sacudirFila(indiceFila) {
  const filaEl = document.getElementById(`fila-${indiceFila}`);
  filaEl.classList.add("sacudir");
  setTimeout(() => filaEl.classList.remove("sacudir"), 500);
}

function actualizarMetricas(intentosUsados) {
  document.getElementById("metrica-intentos").textContent = intentosUsados;
  document.getElementById("contador-intentos").textContent =
    `${intentosUsados} / ${ESTADO.maxIntentos}`;
  document.getElementById("barra-intentos").style.setProperty(
    "--dynamic-width",
    `${(intentosUsados / ESTADO.maxIntentos) * 100}%`
  );
  document.getElementById("metrica-correctas").textContent = ESTADO.letrasCorrectas;
  const exactitud = ESTADO.totalLetras > 0
    ? Math.round((ESTADO.letrasCorrectas / ESTADO.totalLetras) * 100)
    : 0;
  document.getElementById("metrica-exactitud").textContent = `${exactitud}%`;
}

function mostrarPista() {
  document.getElementById("instruccion").textContent = SESION.pista;
}

function mostrarResultado(data) {
  document.querySelector("main.wordle-container").style.display = "none";
  const pantalla = document.getElementById("pantalla-resultado");
  pantalla.classList.add("visible");

  const gano = data.estado === "ganada";
  document.getElementById("resultado-titulo").textContent = gano ? "¡Ganaste!" : "¡Perdiste!";
  document.getElementById("resultado-palabra").textContent = gano
    ? "¡Adivinaste la palabra!"
    : `La palabra era: ${data.palabra}`;
  document.getElementById("resultado-puntaje").textContent = gano
    ? `Puntuación: ${data.puntaje} pts` : "";
}

function mostrarError(msg) {
  const el = document.getElementById("error-juego");
  el.textContent = msg;
  el.classList.add("visible");
}

function ocultarError() {
  document.getElementById("error-juego").classList.remove("visible");
}