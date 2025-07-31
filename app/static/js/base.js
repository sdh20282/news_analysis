const handleUpdateNavigation = () => {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navigation a');

  navLinks.forEach(link => {
    if (currentPath.startsWith(link.getAttribute('href'))) {
      link.classList.add('selected');
    } else {
      link.classList.remove('selected');
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  handleUpdateNavigation();
});
