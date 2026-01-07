document.addEventListener("DOMContentLoaded", function () {
  console.log("cotizacion.js cargado correctamente");

  const form = document.getElementById("registroCotizacionForm");
  if (!form) return;

  const selectServicio = form.querySelector('select[name="servicio"]');
  const inputCantidad = form.querySelector('input[name="cantidad"]');
  const subtotalSpan = document.getElementById("subtotal");
  const totalSpan = document.getElementById("total");

  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");

  function hayCamposObligatoriosVacios() {
    const obligatorios = [
      { name: "cliente", label: "Cliente" },
      { name: "servicio", label: "Servicio" },
      { name: "cantidad", label: "Cantidad" }
    ];

    const faltantes = obligatorios.filter(campo => {
      const el = form.querySelector(`[name="${campo.name}"]`);
      return !el || el.value.trim() === "";
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

  function calcularTotales() {
    if (!selectServicio || !inputCantidad){
      console.warn("Elementos no encontrados");
    return;
  }

    const option = selectServicio.options[selectServicio.selectedIndex];
    console.log("Option:", option);
    /*if (!option || !option.dataset.precio) {
      subtotalSpan.textContent = "0.00";
      totalSpan.textContent = "0.00";
      return;
    }*/

    if (!option) {
      console.warn("No hay opción seleccionada");
      return;
    }

    const rawPrecio = option.getAttribute("data-precio");
    console.log("data-precio:", rawPrecio);

    if (!rawPrecio) {
      subtotalSpan.textContent = "0.00";
      totalSpan.textContent = "0.00";
      return;
    }
    
    const precio = parseFloat(rawPrecio);//const precio = parseFloat(option.dataset.precio);
    const cantidad = parseInt(inputCantidad.value) || 0;
    const total = precio * cantidad;

    subtotalSpan.textContent = total.toFixed(2);
    totalSpan.textContent = total.toFixed(2);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (hayCamposObligatoriosVacios()) return;
    modalConfirmar?.show();
  });

  btnConfirmar?.addEventListener("click", function () {
    modalConfirmar.hide();
    form.submit();
  });

  selectServicio.addEventListener("change", calcularTotales);
  inputCantidad.addEventListener("input", calcularTotales);

  calcularTotales();
});
