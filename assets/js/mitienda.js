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

// Enviar datos al back
const URL = "http://127.0.0.1:5000/"
let session = localStorage.getItem("session")
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
            let card = document.createElement("div")
            card.classList.add("card-group")
            card.innerHTML = `
                <a href="comprarProducto.html" class="card-image" draggable="false">
                    <img src="static/imagenes/${product.imagen}" alt="producto" draggable="false">
                </a>
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

document.getElementById("AddProductContent").addEventListener("submit", (e) => {
    e.preventDefault()
    var formData = new FormData()
    formData.append("codigo", document.getElementById("codigo").value)
    formData.append("producto", document.getElementById("producto").value)
    formData.append("precio", document.getElementById("precio").value)
    formData.append("descripcion", document.getElementById("desc").value)
    formData.append("categoria", document.getElementById("categoria").value)
    formData.append("vendedor", session)
    formData.append("imagen", document.getElementById("imagen").files[0])
    
    fetch(URL + "agregar-producto", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
    })
})