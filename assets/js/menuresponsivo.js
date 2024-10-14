        // Seleccionar el botón hamburguesa y el menú
        const hamburger = document.getElementById('hamburger');
        const menu = document.getElementById('menu');

        // Agregar un evento de clic al botón hamburguesa
        hamburger.addEventListener('click', () => {
            // Alternar la clase 'active' en el menú
            menu.classList.toggle('active');

            // Cambiar apariencia del botón hamburguesa
            hamburger.classList.toggle('open');
        });

        // Cambiar apariencia del botón hamburguesa
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('open');
        });