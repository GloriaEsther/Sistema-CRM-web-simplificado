document.addEventListener("DOMContentLoaded", function () {
    var modal = new bootstrap.Modal(document.getElementById('resultadoModal'));
    modal.show();
    setTimeout(function () {
      window.location.href = "{% url 'inicio' %}";
    }, 3000);
    
  });