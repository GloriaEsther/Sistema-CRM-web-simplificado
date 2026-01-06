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

  if (!form) return;

  function hayCamposObligatoriosVacios() {
    const obligatorios = [
      { name: "cliente", label: "Cliente" },
      { name: "servicio", label: "Servicio" },
      { name: "cantidad", label: "Cantidad" }
    ];

    const faltantes = obligatorios.filter(campo => {
      const el = form.querySelector(`[name="${campo.name}"]`);
      return !el || !el.value;
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
    modalConfirmar.show();
  });

  btnConfirmar.addEventListener("click", function () {
    modalConfirmar.hide();
    form.submit();
  });

  function calcularTotales() {
    if (!selectServicio || !inputCantidad) return;

    const opcionSeleccionada = selectServicio.options[selectServicio.selectedIndex];
    const precio = parseFloat(opcionSeleccionada.dataset.precio || 0);
    const cantidad = parseInt(inputCantidad.value || 1);

    const subtotal = precio * cantidad;
    const total = subtotal; // por ahora iguales

    subtotalSpan.textContent = subtotal.toFixed(2);
    totalSpan.textContent = total.toFixed(2);
    //debug temporal
    console.log({
      precio:precio,
      cantidad:cantidad,
      opcion:opcionSeleccionada
    });
  }

    // Forzar cálculo inicial
  setTimeout(() => {
    calcularTotales();
  }, 100);

  // Eventos
  selectServicio.addEventListener("change", calcularTotales);
  inputCantidad.addEventListener("input", calcularTotales);

  // Calcular al cargar
  calcularTotales();
});
