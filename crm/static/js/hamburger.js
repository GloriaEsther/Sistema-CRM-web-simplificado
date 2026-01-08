document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger-menu");
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("menu-overlay");

  hamburger?.addEventListener("click", () => {
    menu.classList.toggle("active");
    overlay.classList.toggle("active");
  });

  overlay?.addEventListener("click", () => {
    menu.classList.remove("active");
    overlay.classList.remove("active");
  });
});
