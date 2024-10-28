// Agregar producto: Abrir formulario
document.getElementById("addProductBtn").addEventListener("click", () => {
    document.getElementById("addProduct").classList.add("active")
    document.getElementById("AddProductContent").classList.add("active")
})

// Agregar producto: Cerrar formulario
document.getElementById("cancelProductBtn").addEventListener("click", () => {
        document.getElementById("addProduct").classList.remove("active")
        document.getElementById("AddProductContent").classList.remove("active")
})

// Editar perfil: Abrir formulario
document.getElementById("editProfileBtn").addEventListener("click", () => {
    document.getElementById("editarPerfil").classList.add("active")
    document.getElementById("editarPerfilContent").classList.add("active")
})


// Editar perfil: Cerrar formulario
document.getElementById("cancelPerfilBtn").addEventListener("click", () => {
    document.getElementById("editarPerfil").classList.remove("active")
    document.getElementById("editarPerfilContent").classList.remove("active")
})

// Mostrar productos
// const URL = "https://nomarket.pythonanywhere.com/"
const URL = "http://127.0.0.1:5000/"
let session = localStorage.getItem("session")
let productos = []

window.addEventListener("load", () => {
    document.getElementById("nombreTienda").innerHTML = session
    var formData = new FormData()
    formData.append("vendedor", session)
    fetch(URL + "mostrar-productos", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        let cards = document.getElementById("cards")
        let productosCantidad = 0
        for(let product of data) {
            productos.push(product)
            let card = document.createElement("div")
            card.classList.add("card-group")
            card.innerHTML = `
                <p class="card-image" id="cardImage" draggable="false">
                    <img src="${product.imagen}" alt="${product.codigo}" draggable="false">
                </p>
                <div class="card-content">
                    <p>${product.categoria}</p>
                    <h3>${product.producto}</h3>
                    <span>$${product.precio}</span>
                </div>
            `
            productosCantidad++
            if (productosCantidad == 1) {
                document.getElementById("productosCantidad").innerHTML = `${productosCantidad} producto`
            } else {
                document.getElementById("productosCantidad").innerHTML = `${productosCantidad} productos`
            }
            cards.appendChild(card)
        }
    })
})

// Agregar productos
document.getElementById("AddProductContent").addEventListener("submit", (e) => {
    e.preventDefault()
    var formData = new FormData()
    formData.append("codigo", document.getElementById("codigo").value)
    formData.append("producto", document.getElementById("producto").value)
    formData.append("precio", document.getElementById("precio").value)
    formData.append("descripcion", document.getElementById("desc").value)
    formData.append("categoria", document.getElementById("categoria").value)
    formData.append("vendedor", session)
    formData.append("imagen", document.getElementById("imagen").value)
    
    fetch(URL + "agregar-producto", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.mensaje)
        if (data.mensaje == "Producto agregado") {
            document.getElementById("errorContainer").classList.add("success")
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje

            document.getElementById("producto").value = ""
            document.getElementById("codigo").value = ""
            document.getElementById("categoria").value = ""
            document.getElementById("desc").value = ""
            document.getElementById("precio").value = ""
            document.getElementById("imagen").value = ""
        } else {
            document.getElementById("errorContainer").classList.remove("success")
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje
        }
    })
})

// Cerrar mensaje de error
document.getElementById("closeError").addEventListener("click", () => {
    document.getElementById("error").classList.remove("active")
})

// Editar producto: Abrir formulario
let productoCodigo = ""
document.getElementById("cards").addEventListener("click", (e) => {
    if (e.target.tagName == "IMG") {
        productoCodigo = e.target.alt
        document.getElementById("editProduct").classList.add("active")
        document.getElementById("editProductContent").classList.add("active")
        for (let i of productos) {
            if(e.target.alt == i.codigo) {
                document.getElementById("editar_codigo").value = i.codigo
                document.getElementById("nuevo_producto").value = i.producto
                document.getElementById("nuevo_precio").value = i.precio
                document.getElementById("nuevo_desc").value = i.descripcion
                document.getElementById("nuevo_categoria").value = i.categoria
                document.getElementById("nuevo_imagen").value = i.imagen
            }
        }
    }
})

// Editar producto: Cerrar formulario
document.getElementById("cancelEditBtn").addEventListener("click", () => {
    document.getElementById("editProduct").classList.remove("active")
    document.getElementById("editProductContent").classList.remove("active")
})

// Editar producto: Enviar datos al back
document.getElementById("editProductContent").addEventListener("submit", (e) => {
    e.preventDefault()
    var editarProducto = new FormData()
    editarProducto.append("codigo", document.getElementById("editar_codigo").value)
    editarProducto.append("producto", document.getElementById("nuevo_producto").value)
    editarProducto.append("precio", document.getElementById("nuevo_precio").value)
    editarProducto.append("descripcion", document.getElementById("nuevo_desc").value)
    editarProducto.append("categoria", document.getElementById("nuevo_categoria").value)
    editarProducto.append("imagen", document.getElementById("nuevo_imagen").value)
    fetch(URL + "editar-producto", {
        method: "PUT",
        body: editarProducto,
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.mensaje == "Producto modificado") {
            document.getElementById("errorContainer").classList.add("success")
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje

            document.getElementById("editProduct").classList.remove("active")
            document.getElementById("editProductContent").classList.remove("active")
        }
    })
    .catch((error) => alert(error))
})

// Eliminar producto: Abrir menú
document.getElementById("deleteProductBtn").addEventListener("click", () => {
    document.getElementById("deleteproduct").classList.add("active")
    document.getElementById("deleteProductContent").classList.add("active")
})

// Eliminar producto: Cerrar menú
document.getElementById("cancelDelete").addEventListener("click", () => {
    document.getElementById("deleteproduct").classList.remove("active")
    document.getElementById("deleteProductContent").classList.remove("active")
})

// Eliminar producto: Enviar datos al back
document.getElementById("confirmDelete").addEventListener("click", () => {
    var eliminarProducto = new FormData()
    eliminarProducto.append("codigo", productoCodigo)
    fetch(URL + `eliminar-producto`, {
        method: "POST",
        body: eliminarProducto,
    })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => alert(error))
})