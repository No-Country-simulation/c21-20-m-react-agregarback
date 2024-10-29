// Abrir filtros
document.getElementById("filterBtn").addEventListener("click", () => {
    document.getElementById("filterShadow").classList.add("active")
    document.getElementById("filter").classList.add("active")
})

// Cerrar filtros
document.getElementById("filterShadow").addEventListener("click", (e) => {
    if (e.target.id == "filterShadow") {
        document.getElementById("filterShadow").classList.remove("active")
    document.getElementById("filter").classList.remove("active")
    }
})

// Recibir datos del back
const URL = "https://nomarket.pythonanywhere.com/"
// const URL = "http://127.0.0.1:5000/"


window.addEventListener("load", () => {
    fetch(URL + "mostrar-all-productos")
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        for(let prod of data) {
            let cards = document.getElementById("cards")
            let card = document.createElement("div")
            card.classList.add("card-group")
            card.innerHTML = `
                <p class="card-image" onClick="productoSeleccionado(event)">
                    <img src="${prod.imagen}" alt="${prod.codigo}">
                </p>
                <div class="card-content">
                    <p>${prod.vendedor}</p>
                    <h3>${prod.producto}</h3>
                    <span>$${prod.precio}</span>
                </div>
                `
            cards.appendChild(card)
        }
    })
})

//Seleccionar un producto
function productoSeleccionado(e) {
    localStorage.setItem("productoSeleccionado", e.target.alt)
    location.href = "comprarProducto.html"
}