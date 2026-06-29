const RUTAS_INICIAR = {
    "palabra_del_dia": "/juegos/wordle/iniciar",
    "rosco":           "/juegos/rosco/iniciar",
    "contexto":        "/juegos/contexto/iniciar"
};

const RUTAS_JUGAR = {
    "palabra_del_dia": "/juegos/wordle/jugar",
    "rosco":           "/juegos/rosco/jugar",
    "contexto":        "/juegos/contexto/jugar"
};

async function enviarTematica(e) {
    e.preventDefault();

    const tematica = document.getElementById("input-tematica").value.trim();
    const errorEl = document.getElementById("error-tematica");
    const btn = document.getElementById("btn-jugar");

    if (!tematica) {
        errorEl.textContent = "Ingresá una temática antes de continuar.";
        errorEl.style.display = "block";
        return;
    }

    errorEl.style.display = "none";
    btn.textContent = "Generando...";
    btn.disabled = true;

    try {
        const res = await fetch(RUTAS_INICIAR[JUEGO], {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tematica })
        });

        const data = await res.json();

        if (data.error) {
            errorEl.textContent = data.error;
            errorEl.style.display = "block";
            btn.textContent = "Comenzar a jugar";
            btn.disabled = false;
            return;
        }

        window.location.href = `${RUTAS_JUGAR[JUEGO]}?sesion=${data.id_sesion}`;

    } catch {
        errorEl.textContent = "Error de conexión. Intentá de nuevo.";
        errorEl.style.display = "block";
        btn.textContent = "Comenzar a jugar";
        btn.disabled = false;
    }
}