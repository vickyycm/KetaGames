document.addEventListener("DOMContentLoaded", () => {

    inicializarRosco();

    window.addEventListener("resize", renderizarRosco);

    document
        .getElementById("btn-responder")
        .addEventListener(
            "click",
            responderPregunta
        );

    document
        .getElementById("respuesta-input")
        .addEventListener(
            "input",
            () => {
                document.getElementById(
                    "error-juego"
                ).textContent = "";
            }
        );

    document
        .getElementById("btn-pasar")
        .addEventListener(
            "click",
            pasarPregunta
        );

    document
        .getElementById("respuesta-input")
        .addEventListener(
            "keydown",
            e => {
                if (e.key === "Enter") {
                    responderPregunta();
                }
            }
        );

    document
        .getElementById("btn-volver-inicio")
        .addEventListener(
            "click",
            () => {
                window.location.href = "/";
            }
        );
});

function inicializarRosco() {
    document.getElementById(
        "tematica-actual"
    ).textContent = SESION.tematica;

    actualizarPantalla();
    renderizarRosco();
}

function actualizarPantalla() {
    document.getElementById(
        "letra-actual"
    ).textContent = SESION.letra_actual || "-";

    document.getElementById(
        "pregunta-actual"
    ).textContent = SESION.definicion || "";

    document.getElementById(
        "correctas"
    ).textContent = SESION.aciertos || 0;

    document.getElementById(
        "incorrectas"
    ).textContent = SESION.errores || 0;

    document.getElementById(
        "score-valor"
    ).textContent = SESION.puntaje || 0;
}

function renderizarRosco() {
    const contenedor = document.getElementById("rosco");
    if (!contenedor) return;

    contenedor.innerHTML = "";

    const letras = Object.keys(SESION.preguntas);
    if (letras.length === 0) return;

    const anchoContenedor = contenedor.clientWidth || 650; 
    
    const centro = anchoContenedor / 2;
    
    const radio = anchoContenedor * 0.40;

    letras.forEach((letra, index) => {
        const pregunta = SESION.preguntas[letra];
        const nodo = document.createElement("div");

        nodo.classList.add("letra");
        contenedor.appendChild(nodo); 

        const mitadLetra = nodo.offsetWidth / 2 || 25; 

        const angulo =
            ((Math.PI * 2) / letras.length) * index - Math.PI / 2;

        const x = centro + radio * Math.cos(angulo) - mitadLetra;
        const y = centro + radio * Math.sin(angulo) - mitadLetra;

        nodo.style.left = `${x}px`;
        nodo.style.top = `${y}px`;
        nodo.textContent = letra;

        if (letra === SESION.letra_actual) {
            nodo.classList.add("letra-activa");
        }

        if (pregunta.estado === "correcta") {
            nodo.classList.add("letra-correcta");
        }

        if (pregunta.estado === "incorrecta") {
            nodo.classList.add("letra-incorrecta");
        }

        if (pregunta.estado === "pasada") {
            nodo.classList.add("letra-pasada");
        }
    });
}

async function responderPregunta() {
    const respuesta = document.getElementById("respuesta-input").value.trim();

    if (!respuesta) {
        mostrarError("Ingresá una respuesta");
        setTimeout(() => {
            document.getElementById("error-juego").textContent = "";
        }, 3000);
        return;
    }

    const res = await fetch("/juegos/rosco/responder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id_sesion: SESION.id_sesion,
            letra: SESION.letra_actual,
            respuesta
        })
    });

    const data = await res.json();

    if (data.error) {
        mostrarError(data.error);
        return;
    }

    actualizarSesion(data);
    document.getElementById("respuesta-input").value = "";
}

async function pasarPregunta() {
    const res = await fetch("/juegos/rosco/pasar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id_sesion: SESION.id_sesion,
            letra: SESION.letra_actual
        })
    });

    const data = await res.json();

    if (data.error) {
        mostrarError(data.error);
        return;
    }

    actualizarSesion(data);
}

function actualizarSesion(data) {
    SESION.preguntas = data.preguntas;
    SESION.estado = data.estado;
    SESION.puntaje = data.puntaje;
    SESION.aciertos = data.aciertos;
    SESION.errores = data.errores;
    SESION.letra_actual = data.letra_actual;
    SESION.definicion = data.definicion;

    const respuestaCorrecta = document.getElementById("respuesta-correcta");

    if (data.correcta === false && data.respuesta_correcta) {
        respuestaCorrecta.textContent = `La respuesta correcta era: ${data.respuesta_correcta}`;
    } else {
        respuestaCorrecta.textContent = "";
    }

    actualizarPantalla();
    renderizarRosco();

    if (data.estado === "finalizada") {
        mostrarResultado(data);
    }
}

function mostrarResultado(data) {
    document.querySelector(".rosco-container").style.display = "none";
    const pantalla = document.getElementById("pantalla-resultado");
    pantalla.style.display = "flex";

    document.getElementById("resultado-titulo").textContent = "Rosco finalizado";
    document.getElementById("resultado-puntaje").textContent = `Puntaje: ${data.puntaje}`;
    document.getElementById("resultado-correctas").textContent = `Correctas: ${data.aciertos}`;
    document.getElementById("resultado-incorrectas").textContent = `Incorrectas: ${data.errores}`;
}

function mostrarError(msg) {
    const el = document.getElementById("error-juego");
    el.textContent = msg;
    el.classList.add("visible");
}