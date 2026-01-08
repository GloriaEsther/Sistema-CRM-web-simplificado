document.addEventListener("DOMContentLoaded", function () {
  const modalEl = document.getElementById("modalEliminar");
  if (!modalEl) return;

  const modal = new bootstrap.Modal(modalEl);
  const nombreEl = document.getElementById("modalEliminarNombre");
  const confirmarEl = document.getElementById("modalEliminarConfirmar");

  document.querySelectorAll(".btn-eliminar").forEach(btn => {
    btn.addEventListener("click", e => {
      e.preventDefault();

      const id = btn.dataset.id;
      const nombre = btn.dataset.nombre;
      const baseUrl = btn.dataset.url; 
      confirmarEl.href = baseUrl.replace("0", id);
      nombreEl.textContent = nombre;

      modal.show();
    });
  });

});
