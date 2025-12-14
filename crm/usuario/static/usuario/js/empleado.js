document.addEventListener("DOMContentLoaded", function () {
    // Obtener elementos
    const RolContainer = document.getElementById("rolContainer");
    const RolInput = document.getElementById("id_rol");
    const nombreInput = document.getElementById("id_nombre");
    const apellidopaternoInput=document.getElementById("id_apellidopaterno");
    const apellidomaternoInput=document.getElementById("id_apellidomaterno");
    const numerotelInput=document.getElementById("id_numerotel");
    const correoInput=document.getElementById("id_correo");
    
    const btnGuardar = document.getElementById("btnGuardar");
    const form = document.getElementById("EmpleadoForm");
    // Iniciar objetos de modal
    // Se inicializan aquí para que el código pueda llamarlos con .show()
    const modalConfirmar = new bootstrap.Modal(document.getElementById("confirmModal"));
    const modalContrasena = new bootstrap.Modal(document.getElementById("coninvalida"));
    const modalFaltantes = new bootstrap.Modal(document.getElementById("faltantesModal")); 

    const btnConfirmar = document.getElementById("confirmarOpcionales");
    const btnDescartar = document.getElementById("descartarOpcionales");
    const btnAceptar = document.getElementById("confirmar");

    function camposVacios() {
        const obligatorios = [
            { id: "id_nombre", label: "Nombre" },
            { id: "id_apellidopaterno", label: "Apellido Paterno" },
            { id: "id_apellidomaterno", label: "Apellido Materno" },
            { id: "id_numerotel", label: "Número Telefónico" },
            { id: "id_correo", label: "Correo Electrónico" },
            { id: "id_contrasena", label: "Contraseña" },
            { id: "id_rol", label: "Rol", tipo: "select"},
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
        
        modalConfirmar.show();
        form.submit();
    });

    btnAceptar.addEventListener("click", function () {
        modalContrasena.hide();
    });

    btnConfirmar.addEventListener("click", function () {
        modalConfirmar.hide();
        form.submit();
    });

    btnDescartar.addEventListener("click", function () {
        if (RolInput) RolInput.value = "";
        if (nombreInput) nombreInput.value = "";
        if (apellidopaternoInput) apellidopaternoInput.value="";
        if (apellidomaternoInput) apellidomaternoInput.value= "";
        if (numerotelInput) numerotelInput.value= "";
        if (correoInput) correoInput.value= "";
        if (contrasenaInput) contrasenaInput.value= "";
        form.submit();
    });
});