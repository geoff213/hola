document.addEventListener('DOMContentLoaded', function() {
    // Agregar evento click a todos los botones "Ver Más"
    const buttons = document.querySelectorAll('.image-box button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const description = this.previousElementSibling.textContent;
            alert(`Más información: ${description}`);
        });
    });

    // Cambiar el color de fondo al hacer hover sobre las imágenes
    const images = document.querySelectorAll('.image-box img');
    images.forEach(image => {
        image.addEventListener('mouseover', function() {
            this.parentNode.style.backgroundColor = '#e0f7fa';
        });
        image.addEventListener('mouseout', function() {
            this.parentNode.style.backgroundColor = 'white';
        });
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const mainContent = document.getElementById('main-content');
    const galleryBtn = document.getElementById('gallery-btn');
    const aboutBtn = document.getElementById('about-btn');
    const contactBtn = document.getElementById('contact-btn');

 
    function loadGalleryContent() {
        mainContent.innerHTML = '<h2>Contenido de la Galería</h2>';
       
    }

    function loadAboutContent() {
        mainContent.innerHTML = '<h2>Acerca de Nosotros</h2>';
        
    }

    function loadContactContent() {
        mainContent.innerHTML = '<h2>Contacto</h2>';

    }

    loadGalleryContent();
    galleryBtn.addEventListener('click', loadGalleryContent);
    aboutBtn.addEventListener('click', loadAboutContent);
    contactBtn.addEventListener('click', loadContactContent);
});

function agregarAlCarrito(idProducto) {
    fetch('/agregar_al_carrito/' + idProducto)
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}