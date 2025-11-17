document.addEventListener("DOMContentLoaded", () => {
    let primary = localStorage.getItem("color1");
    let secondary = localStorage.getItem("color2");

    if (primary) document.documentElement.style.setProperty("--primary", primary);
    if (secondary) document.documentElement.style.setProperty("--secondary", secondary);
});

function openColorModal() {
    new bootstrap.Modal(document.getElementById("colorModal")).show();
}

function saveColors() {
    let c1 = document.getElementById("color1").value;
    let c2 = document.getElementById("color2").value;

    localStorage.setItem("color1", c1);
    localStorage.setItem("color2", c2);

    document.documentElement.style.setProperty("--primary", c1);
    document.documentElement.style.setProperty("--secondary", c2);

    bootstrap.Modal.getInstance(document.getElementById("colorModal")).hide();
}

