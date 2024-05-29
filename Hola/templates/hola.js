document.addEventListener('DOMContentLoaded', function() {
    const mainContent = document.getElementById('main-content');
    const cartContainer = document.getElementById('cart-container');
    const cartItemsList = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const checkoutBtn = document.getElementById('checkout-btn');
    const productModal = $('#productModal');
    const productModalLabel = document.getElementById('productModalLabel');
    const productModalImage = document.getElementById('productModalImage');
    const productModalDescription = document.getElementById('productModalDescription');
    const productModalButton = document.getElementById('productModalButton');

    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    let currentProduct = {};

    function updateCart() {
        cartItemsList.innerHTML = '';
        cartItems.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = item.description;
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Eliminar';
            removeBtn.addEventListener('click', () => {
                cartItems.splice(index, 1);
                updateCart();
            });
            li.appendChild(removeBtn);
            cartItemsList.appendChild(li);
        });
        cartCount.textContent = cartItems.length;
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
    }

    function loadGalleryContent() {
        mainContent.innerHTML = `
            <section class="image-section">
                <h2></h2>
                <div class="image-gallery row">
                    <div class="image-box col-sm-6 col-md-4 col-lg-3">
                        <img src="img/hola.avif" alt="Imagen 1">
                        <div class="description">Producto 1</div>
                        <button data-title="Producto 1" data-description="Descripción del Producto 1" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                    <div class="image-box col-sm-6 col-md-4 col-lg-3">
                        <img src="img/hola.avif" alt="Imagen 2">
                        <div class="description">Producto 2</div>
                        <button data-title="Producto 2" data-description="Descripción del Producto 2" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                    <div class="image-box col-sm-6 col-md-4 col-lg-3">
                        <img src="img/hola.avif" alt="Imagen 3">
                        <div class="description">Producto 3</div>
                        <button data-title="Producto 3" data-description="Descripción del Producto 3" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                    <div class="image-box col-sm-6 col-md-4 col-lg-3">
                        <img src="img/hola.avif" alt="Imagen 4">
                        <div class="description">Producto 4</div>
                        <button data-title="Producto 4" data-description="Descripción del Producto 4" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                     <div class="image-box col-sm-6 col-md-4 col-lg-3">
                       <img src="img/hola.avif" alt="Imagen 4">
                       <div class="description">Producto 4</div>
                       <button data-title="Producto 4" data-description="Descripción del Producto 4" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                    <div class="image-box col-sm-6 col-md-4 col-lg-3">
                       <img src="img/hola.avif" alt="Imagen 4">
                       <div class="description">Producto 4</div>
                       <button data-title="Producto 4" data-description="Descripción del Producto 4" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
                       <div class="image-box col-sm-6 col-md-4 col-lg-3">
                       <img src="img/hola.avif" alt="Imagen 4">
                       <div class="description">Producto 4</div>
                       <button data-title="Producto 4" data-description="Descripción del Producto 4" data-img="img/hola.avif">Ver Detalles</button>
                    </div>
            </section>
            
        `;
        addImageBoxEvents();
    }

    function addImageBoxEvents() {
        const buttons = document.querySelectorAll('.image-box button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const title = this.getAttribute('data-title');
                const description = this.getAttribute('data-description');
                const img = this.getAttribute('data-img');

                currentProduct = { title, description, img };

                productModalLabel.textContent = title;
                productModalDescription.textContent = description;
                productModalImage.src = img;

                productModal.modal('show');
            });
        });

        productModalButton.addEventListener('click', function() {
            cartItems.push(currentProduct);
            updateCart();
            productModal.modal('hide');
        });
    }

    function loadAboutContent() {
        mainContent.innerHTML = '<h2>Acerca de Nosotros</h2><p>Información sobre nosotros...</p>';
    }

    function loadContactContent() {
        mainContent.innerHTML = `
            <h2>Contacto</h2>
            <form id="contact-form">
                <div class="form-group">
                    <label for="name">Nombre:</label>
                    <input type="text" id="name" name="name" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="email">Correo Electrónico:</label>
                    <input type="email" id="email" name="email" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="message">Mensaje:</label>
                    <textarea id="message" name="message" class="form-control" rows="4" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Enviar Mensaje</button>
            </form>
        `;
        addFormSubmitEvent();
    }

    function addFormSubmitEvent() {
        const form = document.getElementById('contact-form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = form.elements['name'].value;
            const email = form.elements['email'].value;
            const message = form.elements['message'].value;

            console.log('Nombre:', name);
            console.log('Correo Electrónico:', email);
            console.log('Mensaje:', message);

            const contactData = {
                name: name,
                email: email,
                message: message
            };

            let contacts = JSON.parse(localStorage.getItem('contacts')) || [];
            contacts.push(contactData);
            localStorage.setItem('contacts', JSON.stringify(contacts));

            form.reset();
        });
    }

    if (mainContent) {
        loadGalleryContent();
    }

    const galleryBtn = document.getElementById('gallery-btn');
    const aboutBtn = document.getElementById('about-btn');
    const contactBtn = document.getElementById('contact-btn');
    const cartBtn = document.getElementById('cart-btn');

    if (galleryBtn) {
        galleryBtn.addEventListener('click', function(event) {
            event.preventDefault();
            loadGalleryContent();
        });
    }

    if (aboutBtn) {
        aboutBtn.addEventListener('click', function(event) {
            event.preventDefault();
            loadAboutContent();
        });
    }

    if (contactBtn) {
        contactBtn.addEventListener('click', function(event) {
            event.preventDefault();
            loadContactContent();
        });
    }

    if (cartBtn) {
        cartBtn.addEventListener('click', function(event) {
            event.preventDefault();
            cartContainer.style.display = cartContainer.style.display === 'block' ? 'none' : 'block';
        });
    }

    updateCart();
});
