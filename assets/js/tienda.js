// Recibir datos del back
const URL = "https://nomarket.pythonanywhere.com/"
// const URL = "http://127.0.0.1:5000/"

let tiendaSeleccionada = localStorage.getItem("tiendaSeleccionada")
window.addEventListener("load", () => {
    document.getElementById("nombreTienda").innerHTML = tiendaSeleccionada
    var formData = new FormData()
    formData.append("vendedor", tiendaSeleccionada)
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