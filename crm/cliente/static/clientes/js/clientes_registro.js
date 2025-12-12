document.addEventListener("DOMContentLoaded", function () {
    const nombreInput = document.getElementById("id_nombre");
    const apellidopaternoInput = document.getElementById("id_apellidopaterno");
    const apellidomaternoInput = document.getElementById("id_apellidomaterno");
    const numerotelcliInput = document.getElementById("id_numerotelcli");
    const correoInput = document.getElementById("id_correo");
    const rfcInput =document.getElementById("id_rfc");
    const direccionInput =document.getElementById("id_direccion");
    const fechanacimientoInput = document.getElementById("id_fecha_nacimiento");
    const fechaultimocontactoInput = document.getElementById("id_fecha_ultimocontacto");

    const frecuenciaCompraContainer = document.getElementById("frecuenciaContainer");
    const frecuenciaCompraInput = document.getElementById("id_frecuencia_compra");
    const estadoClienteContainer = document.getElementById("estado_clienteContainer");
    const estadoClienteInput = document.getElementById("id_estado_cliente");
    const comentariosInput = document.getElementById("id_comentarios");

    const btnGuardar = document.getElementById("btnGuardar");
    const form = document.getElementById("registroClienteForm");
   
    const modalConfirmar = new bootstrap.Modal(document.getElementById("confirmModal"));
    const modalFaltantes = new bootstrap.Modal(document.getElementById("faltantesModal")); 

    const btnConfirmar = document.getElementById("confirmarOpcionales");
    const btnDescartar = document.getElementById("descartarOpcionales");

    if (estadoClienteContainer) {
        estadoClienteContainer.style.display = "block";//siempre visible
        
    }

    const FRECUENTE_ID = '3'; // 3 = Frecuente

    function toggleFrecuencia(selectedValue) {
        if (selectedValue === FRECUENTE_ID) {
            frecuenciaCompraContainer.style.display = "block";
        } else {
            frecuenciaCompraContainer.style.display = "none";
            // Limpiamos el valor para evitar enviar datos incorrectos al servidor
            frecuenciaCompraInput.value = "";
        }
    }
    
    // Establecer el estado inicial al cargar la página (para edición o si ya tiene valor)
    if (estadoClienteInput && frecuenciaCompraContainer) {
        // Obtenemos el valor inicial y ajustamos la visibilidad
        toggleFrecuencia(estadoClienteInput.value); 

        // Escuchar los cambios
        estadoClienteInput.addEventListener("change", function () {
            toggleFrecuencia(this.value);
        });
    }
    
    function camposVacios() {
        const obligatorios = [
            { id: "id_nombre", label: "Nombre" },
            { id: "id_apellidopaterno", label: "Apellido Paterno" },
            { id: "id_apellidomaterno", label: "Apellido Materno" },
            { id: "id_numerotelcli", label: "Número Telefónico" },
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

        const datos =
            (nombreInput && nombreInput.value.trim() !== "") ||
            (apellidopaternoInput && apellidopaternoInput.value.trim() !== "")||
            (apellidomaternoInput && apellidomaternoInput.value.trim() !== "") ||
            (numerotelcliInput && numerotelcliInput.value.trim() !== "") ||
            (correoInput && correoInput.value.trim() !== "") ||
            (rfcInput && rfcInput.value.trim() !== "") ||
            (direccionInput && direccionInput.value.trim() !== "") ||
            (fechanacimientoInput && fechanacimientoInput.value.trim() !== "")||
            (fechaultimocontactoInput && fechaultimocontactoInput.value.trim() !== "") ||
            (frecuenciaCompraInput && frecuenciaCompraInput.value.trim() !== "") ||
            (estadoClienteInput && estadoClienteInput.value.trim() !== "") ||
            (comentariosInput && comentariosInput.value.trim() !== "");

        if (datos) {
            modalConfirmar.show();
        } else {
            form.submit();
        }
    });
    
    btnConfirmar.addEventListener("click", function () {
        modalConfirmar.hide();
        form.submit();
    });

    btnDescartar.addEventListener("click", function () {
        if (nombreInput) nombreInput.value = "";
        if(apellidopaternoInput) apellidopaternoInput.value="";
        if(apellidomaternoInput) apellidomaternoInput.value="";
        if(numerotelcliInput) numerotelcliInput.value="";
        if(correoInput) correoInput.value="";
        if (rfcInput) rfcInput.value = "";
        if (direccionInput) direccionInput.value = "";
        if(fechanacimientoInput) fechanacimientoInput.value="";
        if(fechaultimocontactoInput) fechaultimocontactoInput.value= "";
        if(frecuenciaCompraInput)frecuenciaCompraInput.value = "";
        if (estadoClienteInput) estadoClienteInput.value= "";
        if(comentariosInput) comentariosInput.value= "";
        form.submit();
    });
});