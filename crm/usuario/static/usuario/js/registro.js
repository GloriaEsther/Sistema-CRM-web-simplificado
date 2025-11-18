document.addEventListener("DOMContentLoaded", function () {
    // Obtener elementos
    const rolSelect = document.getElementById("id_rol");
    const localFijoContainer = document.getElementById("localFijoContainer");
    const localFijoInput = document.getElementById("id_local_Fijo");
    const nssInput = document.getElementById("id_nss");
    const rfcInput = document.getElementById("id_rfc");
    const direccionInput = document.getElementById("id_direccion");
    const curpInput = document.getElementById("id_curp");
    const btnGuardar = document.getElementById("btnGuardar");

    const form = document.getElementById("registroForm");

    // Iniicar objetos de modal
    // Se inicializan aquí para que el código pueda llamarlos con .show()
    
    const modalConfirmar = new bootstrap.Modal(document.getElementById("confirmModal"));
    const modalContrasena = new bootstrap.Modal(document.getElementById("coninvalida"));
    const modalFaltantes = new bootstrap.Modal(document.getElementById("faltantesModal")); 
    const btnConfirmar = document.getElementById("confirmarOpcionales");
    const btnDescartar = document.getElementById("descartarOpcionales");
    const btnAceptar = document.getElementById("confirmar");


    // --------------------------------------------------------
    // FUNCIONES Y MANEJADORES DE EVENTOS
    // --------------------------------------------------------

    // Mostrar u ocultar campo Local Fijo según el rol
    function mostrarCampoLocalFijo() {
        if (rolSelect.value === '1') {//  if (rolSelect.value === "Dueño") 
            localFijoContainer.style.display = "block";
        } else {
            localFijoContainer.style.display = "none";
            if (localFijoInput) localFijoInput.value = "";
        }
    }

    rolSelect.addEventListener("change", mostrarCampoLocalFijo);
    mostrarCampoLocalFijo();

    function camposVacios() {
        const obligatorios = [
            { id: "id_nombre", label: "Nombre" },
            { id: "id_apellidopaterno", label: "Apellido Paterno" },
            { id: "id_apellidomaterno", label: "Apellido Materno" },
            { id: "id_numerotel", label: "Número Telefónico" },
            { id: "id_correo", label: "Correo Electrónico" },
            { id: "id_rol", label: "Rol" },
            { id: "id_contrasena", label: "Contraseña" },
        ];

        const faltantes = obligatorios.filter(campo => {
            const el = document.getElementById(campo.id);
            return !el || el.value.trim() === "";
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
            (nssInput && nssInput.value.trim() !== "") ||
            (localFijoInput && localFijoInput.value.trim() !== "") ||
            (rfcInput && rfcInput.value.trim() !== "") ||
            (direccionInput && direccionInput.value.trim() !== "") ||
            (curpInput && curpInput.value.trim() !== "");

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
        if (nssInput) nssInput.value = "";
        if (localFijoInput) localFijoInput.value = "";
        if (rfcInput) rfcInput.value = "";
        if (direccionInput) direccionInput.value = "";
        if (curpInput) curpInput.value = "";
        form.submit();
    });
});