// Simulamos un carrito vacío
let cart = [];

// Función para agregar producto al carrito o incrementar cantidad
function addToCart(product) {
  const existingProduct = cart.find(item => item.id === product.id);

  if (existingProduct) {
    existingProduct.quantity++;
  } else {
    cart.push({...product, quantity: 1});
  }
  
  renderCart();
}

// Función para eliminar un producto del carrito
function removeFromCart(productId) {
  cart = cart.filter(item => item.id !== productId);
  renderCart();
}

// Función para modificar la cantidad de un producto en el carrito
function modifyProductQuantity(productId, newQuantity) {
  const product = cart.find(item => item.id === productId);
  
  if (product && newQuantity > 0) {
    product.quantity = newQuantity;
  } else if (newQuantity === 0) {
    removeFromCart(productId);  // Si la cantidad es 0, eliminamos el producto
  }

  renderCart();
}

// Función para listar los productos en el carrito
function renderCart() {
  const cartList = document.getElementById('cart-list');
  cartList.innerHTML = ''; // Limpiar lista

  if (cart.length === 0) {
    cartList.innerHTML = '<li>Carrito vacío</li>';
    return;
  }

  cart.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      ${item.name} - $${item.price} x 
      <input type="number" min="1" value="${item.quantity}" data-id="${item.id}" class="quantity-input" /> 
      = $${item.price * item.quantity}
      <button class="remove-btn" data-id="${item.id}">Eliminar</button>
    `;

    cartList.appendChild(li);
  });

  // Añadir eventos a los inputs de cantidad y botones de eliminar
  addCartEventListeners();
}

// Función para añadir eventos a inputs y botones en el carrito
function addCartEventListeners() {
  const quantityInputs = document.querySelectorAll('.quantity-input');
  const removeButtons = document.querySelectorAll('.remove-btn');

  // Event listener para modificar la cantidad
  quantityInputs.forEach(input => {
    input.addEventListener('change', (event) => {
      const productId = input.getAttribute('data-id');
      const newQuantity = parseInt(event.target.value);

      modifyProductQuantity(productId, newQuantity);
    });
  });

  // Event listener para eliminar productos
  removeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.getAttribute('data-id');
      removeFromCart(productId);
    });
  });
}

// Agregar evento a los botones "Agregar al carrito"
const buttons = document.querySelectorAll('.add-to-cart');
buttons.forEach(button => {
  button.addEventListener('click', () => {
    const id = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const price = button.getAttribute('data-price');

    const product = {
      id: id,
      name: name,
      price: price
    };

    addToCart(product);
  });
});


