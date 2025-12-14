document.addEventListener("DOMContentLoaded", function () {
    // Obtener elementos
    const localFijoContainer = document.getElementById("localFijoContainer");
    const localFijoInput = document.getElementById("id_local_Fijo");
    const rfcInput = document.getElementById("id_rfc");
    const nombre_negocioInput=document.getElementById("id_nombre_negocio");
    const btnGuardar = document.getElementById("btnGuardar");
    const apellidomaternoInput = document.getElementById("id_apellidopaterno");
    const numerotelInput = document.getElementById("id_numerotel");
    const form = document.getElementById("registroForm");
    
    const modalConfirmar = new bootstrap.Modal(document.getElementById("confirmModal"));
    const modalContrasena = new bootstrap.Modal(document.getElementById("coninvalida"));
    const modalFaltantes = new bootstrap.Modal(document.getElementById("faltantesModal")); 

    const btnConfirmar = document.getElementById("confirmarOpcionales");
    const btnDescartar = document.getElementById("descartarOpcionales");
    const btnAceptar = document.getElementById("confirmar");

    // --------------------------------------------------------
    // Funciones y manejadores de eventos
    // --------------------------------------------------------

    if (localFijoContainer) {
        localFijoContainer.style.display = "block";//siempre visible
        
    }
    // Mostrar/ocultar campos si Local Fijo = "Si"
    if (localFijoInput) {
        if (localFijoInput.value !== "Si") {
            nombre_negocioInput.closest(".col-md-6").style.display = "none";
            rfcInput.closest(".col-md-6").style.display = "none";
        }

        localFijoInput.addEventListener("change", function () {
            if (this.value === "Si") {
                nombre_negocioInput.closest(".col-md-6").style.display = "block";
                rfcInput.closest(".col-md-6").style.display = "block";
            } else {
                nombre_negocioInput.closest(".col-md-6").style.display = "none";
                rfcInput.closest(".col-md-6").style.display = "none";
            }
        });
    }
    function camposVacios() {
        const obligatorios = [
            { id: "id_nombre", label: "Nombre" },
            { id: "id_apellidopaterno", label: "Apellido Paterno" },
            { id: "id_correo", label: "Correo Electrónico" },
            { id: "id_contrasena", label: "Contraseña" },
            { id: "id_local_Fijo", label: "¿Cuenta con un local fijo?", tipo: "select"},
        ];

        const faltantes = obligatorios.filter(campo => {
            const el = document.getElementById(campo.id);
            if (!el) return true;

            if (campo.tipo === "select") {
                return el.value === "" || el.selectedIndex === 0;
            }
            return el.value.trim() === "";
        });

        if (faltantes.length > 0) {
            const lista = document.getElementById("listaFaltantes");
            lista.innerHTML = "";
            faltantes.forEach(c => {
                const li = document.createElement("li");
                li.textContent = c.label;
                lista.appendChild(li);
            });
            modalFaltantes.show();
            return true;
        }
        return false;
    }

    //botones.....

    btnGuardar.addEventListener("click", function (e) {
        e.preventDefault();

        const contrasenaInput = document.getElementById("id_contrasena");
        const contrasena = contrasenaInput.value.trim();
        const regexMayuscula = /[A-Z]/;
        const regexNumero = /\d/;

        if (camposVacios()) return;

        if (contrasena.length < 10 ||
            !regexMayuscula.test(contrasena) ||
            !regexNumero.test(contrasena)
        ) {
            modalContrasena.show();
            return;
        }

        const tieneOpcionales =
            (apellidomaternoInput && apellidomaternoInput.value.trim() !== "") ||
            (numerotelInput && numerotelInput.value.trim() !== "")||
            (rfcInput && rfcInput.value.trim() !== "") ||
            (nombre_negocioInput && nombre_negocioInput.value.trim() !== "");
        if (tieneOpcionales) {
            modalConfirmar.show();
        } else {
            form.submit();
        }
    });

    btnAceptar.addEventListener("click", function () {
        modalContrasena.hide();
    });

    btnConfirmar.addEventListener("click", function () {
        modalConfirmar.hide();
        form.submit();
    });

    btnDescartar.addEventListener("click", function () {
        if(apellidomaternoInput) apellidomaternoInput.value="";
        if(numerotelInput) numerotelInput.value= "";
        if (rfcInput) rfcInput.value = "";
        if(nombre_negocioInput)nombre_negocioInput.value="";
        form.submit();
    });
});