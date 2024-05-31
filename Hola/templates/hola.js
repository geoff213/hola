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
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span>${item.description}</span>
                <div>
                    <input type="number" value="${item.quantity}" min="1" data-index="${index}" class="cart-quantity-input">
                    <button class="btn btn-danger btn-sm remove-btn" data-index="${index}">Eliminar</button>
                </div>
            `;
            cartItemsList.appendChild(li);
        });
        cartCount.textContent = cartItems.length;
        localStorage.setItem('cartItems', JSON.stringify(cartItems));

        document.querySelectorAll('.cart-quantity-input').forEach(input => {
            input.addEventListener('change', updateQuantity);
        });
        document.querySelectorAll('.remove-btn').forEach(button => {
            button.addEventListener('click', removeFromCart);
        });
    }

    function updateQuantity(event) {
        const index = event.target.dataset.index;
        cartItems[index].quantity = parseInt(event.target.value, 10);
        updateCart();
    }

    function removeFromCart(event) {
        const index = event.target.dataset.index;
        cartItems.splice(index, 1);
        updateCart();
    }

    function loadGalleryContent() {
        const products = [
            { title: "Producto 1", description: "Descripción del Producto 1", img: "img/hola.avif" },
            { title: "Producto 2", description: "Descripción del Producto 2", img: "img/hola.avif" },
            { title: "Producto 3", description: "Descripción del Producto 3", img: "img/hola.avif" },
            { title: "Producto 4", description: "Descripción del Producto 4", img: "img/hola.avif" }
        ];

        mainContent.innerHTML = `
            <section class="image-section">
                <h2>Galería de Productos</h2>
                <div class="image-gallery row"></div>
            </section>
        `;

        const imageGallery = mainContent.querySelector('.image-gallery');
        products.forEach(product => {
            const div = document.createElement('div');
            div.className = 'image-box col-sm-6 col-md-4 col-lg-3';
            div.innerHTML = `
                <img src="${product.img}" alt="${product.title}">
                <div class="description">${product.title}</div>
                <button data-title="${product.title}" data-description="${product.description}" data-img="${product.img}">Ver Detalles</button>
            `;
            imageGallery.appendChild(div);
        });

        addImageBoxEvents();
    }

    function addImageBoxEvents() {
        const buttons = document.querySelectorAll('.image-box button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const title = this.getAttribute('data-title');
                const description = this.getAttribute('data-description');
                const img = this.getAttribute('data-img');

                currentProduct = { title, description, img, quantity: 1 };

                productModalLabel.textContent = title;
                productModalDescription.textContent = description;
                productModalImage.src = img;

                productModal.modal('show');
            });
        });
    }

    function loadAboutContent() {
        mainContent.innerHTML = `
            <section class="about-section">
                <h2>Acerca de</h2>
                <p>Esta es la sección de acerca de.</p>
            </section>
        `;
    }

    function loadContactContent() {
        mainContent.innerHTML = `
            <section class="contact-section">
                <h2>Contacto</h2>
                <form id="contact-form">
                    <div class="form-group">
                        <label for="name">Nombre:</label>
                        <input type="text" id="name" name="name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Mensaje:</label>
                        <textarea id="message" name="message" class="form-control" rows="4" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Enviar</button>
                </form>
            </section>
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

            if (!name || !email || !message) {
                alert('Todos los campos son obligatorios.');
                return;
            }

            const contactData = { name, email, message };
            let contacts = JSON.parse(localStorage.getItem('contacts')) || [];
            contacts.push(contactData);
            localStorage.setItem('contacts', JSON.stringify(contacts));

            form.reset();
            alert('Mensaje enviado con éxito.');
        });
    }

    document.getElementById('gallery-btn').addEventListener('click', loadGalleryContent);
    document.getElementById('about-btn').addEventListener('click', loadAboutContent);
    document.getElementById('contact-btn').addEventListener('click', loadContactContent);
    document.getElementById('cart-btn').addEventListener('click', function() {
        cartContainer.style.display = cartContainer.style.display === 'none' ? 'block' : 'none';
    });

    productModalButton.addEventListener('click', function() {
        const existingItemIndex = cartItems.findIndex(item => item.title === currentProduct.title);
        if (existingItemIndex > -1) {
            cartItems[existingItemIndex].quantity += currentProduct.quantity;
        } else {
            cartItems.push(currentProduct);
        }
        updateCart();
        productModal.modal('hide');
    });

    updateCart();
    loadGalleryContent();
});
