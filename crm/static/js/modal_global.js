// -------------------------------------------------------
// 1) MOSTRAR MENSAJES GLOBALES DE DJANGO EN UN SOLO MODAL
// -------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const dataScript = document.getElementById("mensajesData");
    const modalBody = document.getElementById("modalMensajeBody");
    const modalElement = document.getElementById("modalMensaje");

    if (dataScript) {
        let mensajes = [];

        try {
            mensajes = JSON.parse(dataScript.textContent);
        } catch (e) {
            console.error("Error al parsear mensajes:", e);
        }

        if (mensajes.length > 0) {
            modalBody.innerHTML = mensajes
                .map(m => `<div class="alert alert-${m.level}">${m.text}</div>`)
                .join("");

            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }
});

// -------------------------------------------------------
// 2) FUNCIÓN GENERAL PARA MOSTRAR ERRORES DENTRO DE MODALES
// -------------------------------------------------------
function mostrarErroresEnModal(modalSelector, errores) {
    const modal = document.querySelector(modalSelector);
    if (!modal) return;

    const contenedor = modal.querySelector(".error-container");
    if (!contenedor) return;

    contenedor.innerHTML = ""; // limpiar

    if (Array.isArray(errores)) {
        errores.forEach(err => contenedor.innerHTML += `<div>${err}</div>`);
    } else {
        contenedor.innerHTML = `<div>${errores}</div>`;
    }

    contenedor.classList.remove("d-none");

    // Mostrar modal si no está visible
    const instancia = bootstrap.Modal.getInstance(modal) || new bootstrap.Modal(modal);
    instancia.show();
}

// -------------------------------------------------------
// 3) LIMPIAR ERRORES SI SE ABRE OTRO MODAL
// -------------------------------------------------------
document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("show.bs.modal", () => {
        const errorBox = modal.querySelector(".error-container");
        if (errorBox) {
            errorBox.classList.add("d-none");
            errorBox.innerHTML = "";
        }
    });
});

// -------------------------------------------------------
// 4) CAPTURAR ERRORES DEVUELTOS POR AJAX Y MOSTRARLOS
// -------------------------------------------------------
async function enviarFormularioAjax(formSelector, modalSelector, url) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    const formData = new FormData(form);

    const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" }
    });

    const data = await response.json();

    // Caso error de validación
    if (!data.success) {
        mostrarErroresEnModal(modalSelector, data.errors);
        return;
    }

    // Caso éxito → recargar kanban
    location.reload();
}

// -------------------------------------------------------
// 5) EXPONER FUNCIONES PARA USO EN oportunidades.js
// -------------------------------------------------------
window.mostrarErroresEnModal = mostrarErroresEnModal;
window.enviarFormularioAjax = enviarFormularioAjax;

function mostrarModalMensajes(lista) {
    const modalElement = document.getElementById("modalMensaje");
    const modalBody = document.getElementById("modalMensajeBody");
    const modal = new bootstrap.Modal(modalElement);

    modalBody.innerHTML = lista
        .map(m => `<div class="alert alert-${m.level}">${m.text}</div>`)
        .join("");

    modal.show();
}
