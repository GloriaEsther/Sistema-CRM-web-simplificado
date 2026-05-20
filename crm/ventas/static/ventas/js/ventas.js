document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registroVentaForm");
  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");
  const btnDescartar = document.getElementById("descartarOpcionales");

  if (!form) return;

  const contenedor = document.getElementById("contenedor-detalles");
  const btnAgregar = document.getElementById("btn-agregar-articulo");
  const totalFormsInput = document.getElementById("id_set-TOTAL_FORMS") || document.querySelector("[id$='TOTAL_FORMS']");

  // Cálculos Matemáticos
  function calcularTotales() {
    let granTotal = 0;
    const filas = document.querySelectorAll(".detalle-row");

    filas.forEach(fila => {
      // Ignorar filas que estén marcadas para eliminación (en caso de edición)
      const checkboxDelete = fila.querySelector("[id$='-DELETE']");
      if (checkboxDelete && checkboxDelete.checked) {
        fila.style.display = "none"; 
        return; 
      }

      const cantidadInput = fila.querySelector(".cantidad-input");
      const precioInput = fila.querySelector(".precio-input");
      const subtotalInput = fila.querySelector(".subtotal-input");

      const cantidad = parseFloat(cantidadInput?.value) || 0;
      const precio = parseFloat(precioInput?.value) || 0;
      
      // Calculamos el subtotal de la fila
      const subtotal = cantidad * precio;
      
      if (subtotalInput) {
        subtotalInput.value = subtotal.toFixed(2);
      }

      granTotal += subtotal;
    });

    // Inyectamos la suma total en el campo principal de la venta
    const precioTotalInput = document.getElementById("id_preciototal");
    if (precioTotalInput) {
      precioTotalInput.value = granTotal.toFixed(2);
    }
  }

  // --- Misión: Cargar precios desde el catálogo usando JSON ---
  // 1. Leemos el diccionario oculto que Django nos mandó
  const preciosDataElement = document.getElementById("precios-data");
  const catalogosPrecios = preciosDataElement ? JSON.parse(preciosDataElement.textContent) : {servicios: {}, inventario: {}};
  // Escucha cambios en tiempo real en la sección de detalles
  if (contenedor) {
    contenedor.addEventListener("input", function (e) {
      if (e.target.classList.contains("cantidad-input") || e.target.classList.contains("precio-input")) {
        calcularTotales();
      }  
    });

    contenedor.addEventListener("change", function (e) {
      if (e.target.classList.contains("select-servicio") || e.target.classList.contains("select-inventario")) {
        const fila = e.target.closest(".detalle-row");
        const precioInput = fila.querySelector(".precio-input");
        
        // El ID del servicio o inventario que el usuario seleccionó
        const idSeleccionado = e.target.value;
        let precioCatalogo = 0;
        console.log(idSeleccionado)
        // Si seleccionó algo válido (no está vacío)
        if (idSeleccionado) {
          // 2. Buscamos el precio en nuestro diccionario en memoria
          if (e.target.classList.contains("select-servicio")) {
            precioCatalogo = catalogosPrecios.servicios[idSeleccionado] || 0;
            console.log("Servicios:")
            console.log(precioCatalogo)
            const inventarioSelect = fila.querySelector(".select-inventario");
            if (inventarioSelect) inventarioSelect.value = "";
          } else {
            precioCatalogo = catalogosPrecios.inventario[idSeleccionado] || 0;
            console.log("Inventario:")
            console.log(precioCatalogo)
            const servicioSelect = fila.querySelector(".select-servicio");
            if (servicioSelect) servicioSelect.value = "";
          }
        }

        // Asignamos el precio al input
        precioInput.value = parseFloat(precioCatalogo).toFixed(2);
        
        // Recalculamos totales
        calcularTotales();
      }
    });

    // Escucha si borran una fila usando el checkbox DELETE nativo de Django (vistas de edición)
    contenedor.addEventListener("change", function (e) {
      if (e.target.id.endsWith("-DELETE")) {
        calcularTotales();
      }
    });
  }

  // Clonación Dinámica de Filas 
  if (btnAgregar && contenedor && totalFormsInput) {
    btnAgregar.addEventListener("click", function () {
      const filasActuales = document.querySelectorAll(".detalle-row");
      const totalForms = parseInt(totalFormsInput.value);

      // Tomamos la primera fila como plantilla para clonar
      const filaPlantilla = filasActuales[0];
      if (!filaPlantilla) return;

      const nuevaFila = filaPlantilla.cloneNode(true);

      // Limpiamos los valores de los inputs de la nueva fila para que no se clonen con datos
      nuevaFila.querySelectorAll("input, select").forEach(input => {
        if (input.type !== "button") input.value = "";
        
        // Excepción: reestablecer la cantidad mínima por defecto a 1
        if (input.classList.contains("cantidad-input")) input.value = "1";

        // Actualizamos los atributos 'id' y 'name' reemplazando el índice viejo por el nuevo
      const regexIndice = /-(\d+)-/g;
        if (input.id) input.id = input.id.replace(regexIndice, `-${totalForms}-`);
        if (input.name) input.name = input.name.replace(regexIndice, `-${totalForms}-`);
      });

      // Asegurar que las etiquetas labels de la nueva fila apunten a los nuevos IDs
      nuevaFila.querySelectorAll("label").forEach(label => {
        if (label.getAttribute("for")) {
          label.setAttribute("for", label.getAttribute("for").replace(/-(\d+)-/g, `-${totalForms}-`));
        }
      });

      // Configurar el botón de eliminar de la nueva fila clónica
      const btnRemover = nuevaFila.querySelector(".btn-remover-fila");
      if (btnRemover) {
        btnRemover.addEventListener("click", function () {
          // En filas nuevas (no guardadas en BD), simplemente removemos el nodo HTML
          nuevaFila.remove();
          // Decrementamos el total de formularios de control
          totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
          reindexarFilas();
          calcularTotales();
        });
      }

      // Insertamos la nueva fila al final del contenedor
      contenedor.appendChild(nuevaFila);

      // Avisarle a Django que ahora hay un formulario más en el POST
      totalFormsInput.value = totalForms + 1;

      calcularTotales();
    });

    // Configurar comportamiento para el botón de eliminar de la PRIMERA fila inicial
    const primerBtnRemover = document.querySelector(".detalle-row .btn-remover-fila");
    if (primerBtnRemover) {
      primerBtnRemover.addEventListener("click", function (e) {
        const filas = document.querySelectorAll(".detalle-row");
        // Evitamos que borren la única fila si solo queda una
        if (filas.length > 1) {
          e.target.closest(".detalle-row").remove();
          totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
          reindexarFilas();
          calcularTotales();
        } else {
          alert("Una venta debe incluir al menos un artículo o servicio.");
        }
      });
    }
  }

  // Función auxiliar para reordenar los índices secuencialmente si se borra una fila intermedia
  function reindexarFilas() {
    const filas = document.querySelectorAll(".detalle-row");
    filas.forEach((fila, indice) => {
      fila.querySelectorAll("input, select").forEach(input => {
        const regexIndice = /-(\d+)-/g;
        if (input.id) input.id = input.id.replace(regexIndice, `-${indice}-`);
        if (input.name) input.name = input.name.replace(regexIndice, `-${indice}-`);
      });
    });
  }

  function hayCamposObligatoriosVacios() {
    const obligatorios = [
      { id: "id_nombreventa", label: "Nombre de la venta" },
      { id: "id_preciototal", label: "Precio total" },
      { id: "id_estatus_cobro", label: "Estatus de cobro" }
    ];

    const faltantes = obligatorios.filter(campo => {
      const el = document.getElementById(campo.id);
      return !el || el.value.trim() === "";
    });

    // Validar también que al menos una fila de detalles tenga artículos válidos elegidos
    const filasDetalle = document.querySelectorAll(".detalle-row");
    let tieneArticulo = false;
    filasDetalle.forEach(fila => {
      const servicio = fila.querySelector("[id$='-servicio']");
      const inventario = fila.querySelector("[id$='-inventario']");
      if ((servicio && servicio.value !== "") || (inventario && inventario.value !== "")) {
        tieneArticulo = true;
      }
    });

    if (!tieneArticulo) {
      faltantes.push({ id: null, label: "Debe seleccionar al menos un Producto o un Servicio en los detalles" });
    }

    if (faltantes.length > 0 && modalFaltantes) {
      const lista = document.getElementById("listaFaltantes");
      if (lista) {
        lista.innerHTML = "";
        faltantes.forEach(c => {
          const li = document.createElement("li");
          li.textContent = c.label;
          lista.appendChild(li);
        });
      }
      modalFaltantes.show();
      return true;
    }
    return false;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (hayCamposObligatoriosVacios()) return;
    modalConfirmar ? modalConfirmar.show() : form.submit();
  });

  if (btnConfirmar) {
    btnConfirmar.addEventListener("click", function () {
      modalConfirmar.hide();
      form.submit();
    });
  }

  if (btnDescartar) {
    btnDescartar.addEventListener("click", function () {
      form.reset();
      modalConfirmar.hide();
      calcularTotales(); // Resetea el total general a 0
    });
  }

  // Ejecución inicial por si la vista carga datos preexistentes (Edición)
  calcularTotales();
});