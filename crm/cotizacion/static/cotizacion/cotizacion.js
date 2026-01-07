document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registroCotizacionForm");
  const selectServicio = document.querySelector('select[name="servicio"]');
  const inputCantidad = document.querySelector('input[name="cantidad"]');
  const subtotalSpan = document.getElementById("subtotal");
  const totalSpan = document.getElementById("total");

  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");
  const btnDescartar = document.getElementById("descartarOpcionales");

  //if(form){
    function hayCamposObligatoriosVacios() {
      const obligatorios = [
        { name: "cliente", label: "Cliente" },
        { name: "servicio", label: "Servicio" },
        { name: "cantidad", label: "Cantidad" }
      ];

      const faltantes = obligatorios.filter(campo => {
        const el = document.getElementById(campo.id);//const el = form.querySelector(`[name="${campo.name}"]`);
        return !el || el.value.trim()=== "";//return !el || !el.value;
      });

      if (faltantes.length > 0 && modalFaltantes) {
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

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (hayCamposObligatoriosVacios()) return;

      const tieneDatos = Array.from(form.elements).some(el =>
        el.value && el.value.trim() !== ""
      );

      if (tieneDatos && modalConfirmar) {
        modalConfirmar.show();
      } else {
        form.submit();
      }
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
        toggleFrecuencia();
        modalConfirmar.hide();
      });
    }

    function calcularTotales() {
      if (!selectServicio || !inputCantidad) return;

          const selectedOption = selectServicio.options[selectServicio.selectedIndex];
          
          // Obtenemos el precio del atributo data-precio. 
          // Asegúrate que en el HTML diga data-precio="{{ s.precio }}"
          let precio = 0;
          if (selectedOption && selectedOption.value !== "") {
              precio = parseFloat(selectedOption.getAttribute("data-precio")) || 0;
          }

          const cantidad = parseInt(inputCantidad.value) || 0;
          const total = precio * cantidad;

          // Actualizar el texto en el HTML
          if (subtotalSpan) subtotalSpan.textContent = total.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          if (totalSpan) totalSpan.textContent = total.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          
          console.log(`Calculando: ${precio} x ${cantidad} = ${total}`);
    
    }
  // Escuchar cambios
    selectServicio.addEventListener("change", calcularTotales);
    inputCantidad.addEventListener("input", calcularTotales);
    inputCantidad.addEventListener("change", calcularTotales);
   // Calcular una vez al inicio por si hay valores predeterminados
    calcularTotales();
 // }
});
