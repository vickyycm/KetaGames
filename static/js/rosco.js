document.addEventListener("DOMContentLoaded", () => {
    inicializarRosco();

    document
        .getElementById("btn-responder")
        .addEventListener(
            "click",
            responderPregunta
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
    ).textContent =
        SESION.letra_actual || "-";

    document.getElementById(
        "pregunta-actual"
    ).textContent =
        SESION.definicion || "";

    document.getElementById(
        "correctas"
    ).textContent =
        SESION.aciertos || 0;

    document.getElementById(
        "incorrectas"
    ).textContent =
        SESION.errores || 0;

    document.getElementById(
        "score-valor"
    ).textContent =
        SESION.puntaje || 0;
}

function renderizarRosco() {

    const contenedor =
        document.getElementById("rosco");

    contenedor.innerHTML = "";

    const letras =
        Object.keys(SESION.preguntas);

    letras.forEach(letra => {

        const pregunta =
            SESION.preguntas[letra];

        const nodo =
            document.createElement("div");

        nodo.classList.add(
            "rosco-letter"
        );

        nodo.textContent = letra;

        if (
            letra ===
            SESION.letra_actual
        ) {
            nodo.classList.add(
                "actual"
            );
        }

        nodo.classList.add(
            pregunta.estado
        );

        contenedor.appendChild(
            nodo
        );
    });
}

async function responderPregunta() {

    const respuesta =
        document.getElementById(
            "respuesta-input"
        ).value.trim();

    if (!respuesta) {
        mostrarError(
            "Ingresá una respuesta"
        );
        return;
    }

    const res = await fetch(
        "/juegos/rosco/responder",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                id_sesion:
                    SESION.id_sesion,
                letra:
                    SESION.letra_actual,
                respuesta
            })
        }
    );

    const data =
        await res.json();

    if (data.error) {
        mostrarError(data.error);
        return;
    }

    actualizarSesion(data);

    document.getElementById(
        "respuesta-input"
    ).value = "";
}

async function pasarPregunta() {

    const res = await fetch(
        "/juegos/rosco/pasar",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                id_sesion:
                    SESION.id_sesion,
                letra:
                    SESION.letra_actual
            })
        }
    );

    const data =
        await res.json();

    if (data.error) {
        mostrarError(data.error);
        return;
    }

    actualizarSesion(data);
}

function actualizarSesion(data) {

    SESION.preguntas =
        data.preguntas;

    SESION.estado =
        data.estado;

    SESION.puntaje =
        data.puntaje;

    SESION.aciertos =
        data.aciertos;

    SESION.errores =
        data.errores;

    SESION.letra_actual =
        data.letra_actual;

    SESION.definicion =
        data.definicion;

    actualizarPantalla();
    renderizarRosco();

    if (
        data.estado ===
        "finalizada"
    ) {
        mostrarResultado(data);
    }
}

function mostrarResultado(data) {

    document.querySelector(
        ".rosco-container"
    ).style.display = "none";

    const pantalla =
        document.getElementById(
            "pantalla-resultado"
        );

    pantalla.classList.add(
        "visible"
    );

    document.getElementById(
        "resultado-titulo"
    ).textContent =
        "Rosco finalizado";

    document.getElementById(
        "resultado-puntaje"
    ).textContent =
        `Puntaje: ${data.puntaje}`;
}

function mostrarError(msg) {

    const el =
        document.getElementById(
            "error-juego"
        );

    el.textContent = msg;
    el.classList.add("visible");
}
